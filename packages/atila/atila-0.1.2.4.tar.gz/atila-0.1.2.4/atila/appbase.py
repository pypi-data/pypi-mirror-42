import re, sys
from functools import wraps
from urllib.parse import unquote_plus, quote_plus, urljoin
import os
import copy
from rs4 import importer, deco 
from types import FunctionType as function
import inspect
from importlib import reload
from skitai import was as the_was
import time, threading, multiprocessing
from .storage import Storage
from rs4 import evbus
from event_bus.exceptions import EventDoesntExist
import time
import atila
from types import FunctionType
            
RX_RULE = re.compile ("(/<(.+?)>)")
    
class AppBase:    
    use_reloader = False
    debug = False
    auto_mount = True
    contrib_devel = False # make reloadable
    # Session
    securekey = None
    session_timeout = None

    #WWW-Authenticate    
    access_control_allow_origin = None
    access_control_max_age = 0    
    authenticate = None        
    realm = "App"
    users = {}    
    opaque = None
    
    def __init__ (self, *args, **kargs):            
        self.module = None
        self.packagename = None
        self.wasc = None                
        self.logger = None
        self.store = Storage ()
        self.lock = threading.RLock ()
        self.plock = multiprocessing.RLock ()
        self.bus = evbus.EventBus ()
        
        self.mount_p = "/"
        self.path_suffix_len = 0
        self.route_map = {}
        self.route_map_fancy = {}
        self.mount_params = {}
        self.reloadables = {}
        self.last_reloaded = time.time ()        
        self.events = {}        
        self.init_time = time.time ()        
        self.handlers = {}
        
        self._maintern_funcs = {}
        self._package_dirs = []
        self._cleaned = False     
        self._mount_option = {}
        self._started = False
        self._reloading = False        
        self._decos = {"bearer_handler": self.default_bearer_handler}
        self._salt = None
        self._permission_map = {}
        self._jinja2_filters = {}
        self._template_globals = {}
        self._function_specs = {}
        self._current_function_specs = {}
        self._function_names = {}
        self._conditions = {}
        self._need_authenticate = None
        self._cond_check_lock = threading.RLock ()
        self._route_priority = []        
        self._binds_server = [None] * 7
        self._binds_request = [None] * 4        
        
        self.store ["__last_maintern"] = 0.0
        self.store ["__maintern_count"] = 0
        
    def get_resource (self, *args):
        return self.joinpath ("resources", *args)
    
    def joinpath (self, *args):    
        return os.path.normpath (os.path.join (self.home, *args))
                    
    def set_mount_point (self, mount):    
        if not mount:
            self.mount_p = "/"
        elif mount [-1] != "/":
            self.mount_p = mount + "/"
        else:
            self.mount_p = mount
        self.path_suffix_len = len (self.mount_p) - 1
                
    def init (self, module, packagename = "app", mount = "/"):
        self.module = module    
        self.packagename = packagename
        self.set_mount_point (mount)
        
        if self.module:
            self.abspath = self.module.__file__
            if self.abspath [-3:] != ".py":
                self.abspath = self.abspath [:-1]
            self.update_file_info    ()
        
    def __getitem__ (self, k):
        return self.route_map [k]
    
    def get_file_info (self, module):        
        stat = os.stat (module.__file__)
        return stat.st_mtime, stat.st_size
       
    def update_file_info (self):
        stat = os.stat (self.abspath)
        self.file_info = (stat.st_mtime, stat.st_size)
        
    #------------------------------------------------------    
    @property
    def salt (self):
        if self._salt:
            return self._salt
        self._salt = self.securekey.encode ("utf8")
        return self._salt 
    
    def set_default_session_timeout (self, timeout):
        self.session_timeout = timeout
                 
    def set_devel (self, debug = True, use_reloader = True):
        self.debug = debug
        self.use_reloader = use_reloader
    
    # services management ----------------------------------------------
    PACKAGE_DIRS = ["services", "decorative"]
    CONTRIB_DIR = os.path.join (os.path.dirname (atila.__spec__.origin), 'contrib', 'services')
                
    def add_package (self, *names):
        for name in names:
            self.PACKAGE_DIRS.append (name)
    
    def _mount (self, module):
        mount_func = None
        if hasattr (module, "mount"):
            mount_func = module.mount
        elif hasattr (module, "decorate"): # for old ver
            mount_func = module.decorate
                        
        if mount_func:
            if not self.auto_mount and module not in self.mount_params:            
                return        
            params = self.mount_params.get (module, {})
            if params.get ("debug_only") and not self.debug:
                return
            # for app
            setattr (module, "__options__", params)
            setattr (module, "_mount__", params)
            # for app initialzing and reloading
            self._mount_option = params
            try:
                mount_func (self)
                self.log ("{} mounted".format (module.__name__), "info")
            finally:    
                self._mount_option = {}
                
        try:
            self.reloadables [module] = self.get_file_info (module)
        except FileNotFoundError:
            del self.reloadables [module]
            return        
        # find recursively
        self.find_mountables (module)
        
    def find_mountables (self, module):
        for attr in dir (module):
            v = getattr (module, attr)
            try:
                modpath = v.__spec__.origin
            except AttributeError:
                continue
            if not modpath:
                continue            
            if v in self.reloadables:
                continue
            if self.contrib_devel:
                if modpath.startswith (self.CONTRIB_DIR):
                    self._mount (v)
                    continue
            for package_dir in self._package_dirs:
                if modpath.startswith (package_dir):
                    self._mount (v)
                    break
    
    def add_package_dir (self, path):
        if path not in self._package_dirs:
            self._package_dirs.append (path)
            
    def mount_externals (self):
        for module in self.mount_params:            
            if module in self.reloadables:
                continue
            self._mount (module)
        
    def mount (self, maybe_point = None, *modules, **kargs):
        if maybe_point:
            if isinstance (maybe_point, str):                
                kargs ["point"] = maybe_point
            else:
                modules = (maybe_point,) + modules
        for module in modules:
            assert hasattr (module, "mount") or hasattr (module, "decorate")            
            self.add_package_dir (os.path.dirname (module.__spec__.origin))
            self.mount_params [module] = (kargs)
    mount_with = decorate_with = mount    
    
    def umount (self, *modules):
        for module in modules:
            umount_func = None
            if hasattr (module, "umount"):
                umount_func = module.umount
            elif hasattr (module, "dettach"): # for old ver
                umount_func = module.dettach 
            umount_func and umount_func (self)
            self.log ("%s umounted" % module.__name__, "info")
         
    def  umount_all (self):
        self.umount (*tuple (self.reloadables.keys ()))
    dettach_all = umount_all
    
    def maybe_reload (self):
        if time.time () - self.last_reloaded < 1.0:
            return
        
        self._reloading = True
        for module in list (self.reloadables.keys ()):
            try:
                fi = self.get_file_info (module)
            except FileNotFoundError:
                del self.reloadables [module]
                continue
                
            if self.reloadables [module] != fi:
                self.log ("reloading service, %s" % module.__name__, "info")
                self._current_function_specs = {}
                if hasattr (module, "dettach"):
                    module.dettach (self)
                with self.lock:
                    newmodule = reload (module)
                    del self.reloadables [module]
                    self._mount (newmodule)
                    
        self.load_jinja_filters ()
        self.last_reloaded = time.time ()        
        self._reloading = False
    
    def get_func_id (self,  func):
        return ("ns" in self._mount_option and self._mount_option ["ns"] + "." or "") + func.__name__     
        
    # function param saver ------------------------------------------
    def save_function_spec (self, func):
        # save original function spec for preventing distortion by decorating wrapper
        # all wrapper has *args and **karg but we want to keep original function spec for auto parametering call
        func_id = self.get_func_id (func)
        if func_id not in self._function_specs or func_id not in self._current_function_specs:
            # save origin spec
            self._function_specs [func_id] = inspect.getfullargspec(func)
            self._current_function_specs [func_id] = None
    
    def get_function_spec (self, func):        
        # called by websocet_handler 
        func_id = self.get_func_id (func)        
        return self._function_specs.get (func_id)
    
    # logger ----------------------------------------------------------
    def set_logger (self, logger):
        self.logger = logger 
        
    def log (self, msg, type = "info"):
        self.logger (msg, type)
    
    def trace (self):
        self.logger.trace ()
                    
    # app life cycling -------------------------------------------    
    def before_mount (self, f):
        self._binds_server [0] = f        
        return f
    start_up = before_mount
    startup = before_mount
     
    def mounted (self, f):
        self._binds_server [3] = f
        return f
    
    def mounted_or_reloaded (self, f):
        self._binds_server [6] = f
        return f
    
    def before_reload (self, f):
        self._binds_server [5] = f
        return f    
    onreload = before_reload
    reload = before_reload
    
    def reloaded (self, f):
        self._binds_server [1] = f
        return f
    
    def before_umount (self, f):
        self._binds_server [4] = f
        return f
    
    def umounted (self, f):
        self._binds_server [2] = f
        return f
    shutdown = umounted
    
    PHASES = {
        'before_mount': 0,
        'mounted': 3,
        'before_reload': 5,
        'reloaded': 1,
        'before_umount': 4,
        'umounted': 2,
        'mounted_or_reloaded': 6
    }
    def life_cycle (self, phase, obj):
        if phase in ("umounted", "before_reload"):
            self.dettach_all ()
        index = self.PHASES.get (phase)
        func = self._binds_server [index]
        if not func:
            return        
        
        obj.app = self
        try:
            func (obj)
        except:
            if self.logger:
                self.logger.trace ()
            else:
                raise                             

    # Request chains ----------------------------------------------                
    def before_request (self, f):
        self._binds_request [0] = f
        return f
    
    def finish_request (self, f):
        self._binds_request [1] = f
        return f
    
    def failed_request (self, f):
        self._binds_request [2] = f
        return f
    
    def teardown_request (self, f):
        self._binds_request [3] = f
        return f
        
    # Bearer Auth ------------------------------------------------------    
    def bearer_handler (self, f): 
        self._decos ["bearer_handler"] = f
        return f    
    
    def default_bearer_handler (self, was, token):
        claims = was.dejwt (token)    
        if "err" in claims:
          return claims ["err"]
      
    def authorization_handler (self, f):
        self._decos ["auth_handler"] = f
        return f
    
    AUTH_TYPES = ("bearer", "basic", "digest", None)
    def authorization_required (self, authenticate):
        def decorator (f):
            self.save_function_spec (f)
            authenticate_ = authenticate.lower ()
            assert authenticate_ in self.AUTH_TYPES            
            self._need_authenticate = (f.__name__, authenticate_)
            return f
        return decorator
    
    # Session Login ---------------------------------------------------    
    def login_handler (self, f):
        self._decos ["login_handler"] = f
        return f
    
    def login_required (self, f):
        self.save_function_spec (f)
        @wraps(f)
        def wrapper (was, *args, **kwargs):
            _funcs = self._decos.get ("login_handler")
            if _funcs:                
                response = _funcs (was)
                if response is not None:
                    return response
            return f (was, *args, **kwargs)
        return wrapper
    
    # Identifying Member Permission -------------------------- 
    def staff_member_check_handler (self, f):
        self._decos ["staff_member_check_handler"] = f
        return f
    
    def staff_member_required (self, f):
        self.save_function_spec (f)
        @wraps(f)
        def wrapper (was, *args, **kwargs):
            _funcs = self._decos.get ("staff_member_check_handler")
            if _funcs:
                response = _funcs (was)                    
                if response is not None:
                    return response
            return f (was, *args, **kwargs)
        return wrapper
    
    def permission_check_handler (self, f):
        self._decos ["permission_check_handler"] = f
        return f
    
    def permission_required (self, *p):
        if len (p) == 1 and isinstance (p [0], (list, tuple)):
            p = p [0]
        def decorator(f):
            self.save_function_spec (f)
            self._permission_map [f] = p
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                _funcs = self._decos.get ("permission_check_handler")
                if _funcs:
                    response = _funcs (was, self._permission_map [f])                    
                    if response is not None:
                        return response
                return f (was, *args, **kwargs)
            return wrapper
        return decorator
    
    def testpass_required (self, testfunc):
        def decorator(f):
            self.save_function_spec (f)            
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                response = testfunc (was)
                if response is False:
                    return was.response ("403 Permission Denied")
                elif response is not True and response is not None:
                    return response
                return f (was, *args, **kwargs)
            return wrapper
        return decorator
    
    # parameter helpers ------------------------------------------------   
    def _validate_param (self, params, required, ints, floats):
        err= None
        if required:
            for each in required:
                if not params.get (each):
                    return 'parameter required: {}'.format (each)                                                
        if not err and ints:
            for each in ints:
                try: int (params [each])
                except ValueError:
                    return 'integer parameter required: {}'.format (each)                                   
        if err and floats:
            for each in floats:
                try: float (params [each])
                except ValueError:
                    return 'float parameter required: {}'.format (each)                    
            
    def test_param (self, scope, required = None, ints = None, floats = None):
        def decorator(f):
            self.save_function_spec (f)        
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                err = self._validate_param (getattr (was.request, scope), required, ints, floats)
                if err:
                    return was.response.adaptive_error ("400 Bad Request", 'missing or bad {} parameters'.format (scope), 40050, err) 
                return f (was, *args, **kwargs)
            return wrapper
        return decorator
    
    # Automation ------------------------------------------------------    
    def run_before (self, *funcs):
        def decorator(f):
            self.save_function_spec (f)
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                for func in funcs:
                    response = func (was)
                    if response is not None:
                        return response
                return f (was, *args, **kwargs)
            return wrapper
        return decorator
    
    def run_after (self, *funcs):
        def decorator(f):
            self.save_function_spec (f)            
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                response = f (was, *args, **kwargs)
                for func in funcs:
                    func (was)
                return response
            return wrapper
        return decorator
    
    # Conditional Automation ------------------------------------------------------    
    def _check_condition (self, was, key, func, interval, mtime_func):
        now = time.time ()
        with self._cond_check_lock:
            oldmtime, last_check = self._conditions [key]
        
        if not interval or not oldmtime or now - last_check > interval:
            mtime = mtime_func (key)
            if mtime > oldmtime:
                response = func (was, key)
                with self._cond_check_lock:
                    self._conditions [key] = [mtime, now]
                if response is not None:
                    return response
                    
            elif interval:
                with self._cond_check_lock:
                    self._conditions [key][1] = now                        
        
    def if_updated (self, key, func, interval = 1):
        def decorator(f):
            self.save_function_spec (f)
            self._conditions [key] = [0, 0]
            @wrasps(f)
            def wrapper (was, *args, **kwargs):
                response = self._check_condition (was, key, func, interval, was.getlu)
                if response is not None:
                    return response
                return f (was, *args, **kwargs)
            return wrapper
        return decorator
        
    def if_file_modified (self, path, func, interval = 1):
        def decorator(f):
            self.save_function_spec (f)
            self._conditions [path] = [0, 0]            
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                def _getmtime (path): 
                    return os.path.getmtime (path)
                response = self._check_condition (was, path, func, interval, _getmtime)
                if response is not None:
                    return response
                return f (was, *args, **kwargs)
            return wrapper
        return decorator
    
    # Websocket ------------------------------------------------------
    def websocket_config (self, spec, timeout = 60, onopen = None, onclose = None, encoding = "text"):
        def decorator(f):
            self.save_function_spec (f)
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                if not was.wshasevent ():
                    return f (was, *args, **kwargs)
                if was.wsinit ():
                    return was.wsconfig (spec, timeout, encoding)
                elif onopen and was.wsopened ():
                    return onopen (was)
                elif onclose and was.wsclosed ():                    
                    return onclose (was)
            return wrapper
        return decorator
    
    # Templaing -------------------------------------------------------    
    def template_global (self, name):    
        def decorator(f):
            self.save_function_spec (f)
            @wraps(f)
            def wrapper (*args, **kwargs):                
                return f (the_was._get (), *args, **kwargs)
            self._template_globals [name] = wrapper
            return wrapper
        return decorator
    
    def template_filter (self, name):    
        def decorator(f):
            self._jinja2_filters [name] = f
            @wraps(f)
            def wrapper (*args, **kwargs):                
                return f (*args, **kwargs)            
            return wrapper
        return decorator
    
    
    # mainterinancing -------------------------------------------------------
    def maintain (self, f):
        if not self._started:
            assert f.__name__ not in self._maintern_funcs, "maintain func {} is already exists".format (f.__name__)
        self._maintern_funcs [f.__name__] = f
        return f
    
    def maintern (self):
        if not self._maintern_funcs:
            return
        now = time.time ()
        if (now - self.store ["__last_maintern"]) < self.config.get ("maintain_interval", 60):
            return
        
        was = the_was._get ()    
        with self.lock:
            for func in self._maintern_funcs.values ():
                func (was, now, self.store ["__maintern_count"])
        self.store ["__last_maintern"] = now
        self.store ["__maintern_count"] += 1
                
    # Error handling ------------------------------------------------------        
    def render_error (self, error):
        handler = self.handlers.get (error ['code'], self.handlers.get (0))
        if not handler:
            return
        was = the_was._get ()    
        # reset was.app for rendering
        was.app = self
        content =    handler [0] (was, error)
        was.app = None
        return content
        
    def add_error_handler (self, errcode, f, **k):
        self.handlers [errcode] = (f, k)
        
    def error_handler (self, errcode, **k):
        def decorator(f):
            self.add_error_handler (errcode, f, **k)
            @wraps(f)
            def wrapper (*args, **kwargs):
                return f (*args, **kwargs)
            return wrapper
        return decorator
    
    def default_error_handler (self, f):
        self.add_error_handler (0, f)
        return f
    
    defaulterrorhandler = default_error_handler
    errorhandler = error_handler
    
    # URL Building ------------------------------------------------
    def urlfor (self, thing, *args, **kargs):
        if isinstance (thing, FunctionType):
            thing = self._function_names [id (thing)]
        if thing.startswith ("/"):
            return self.basepath [:-1] + self.mount_p [:-1] + thing
        
        script_name_only = "__resource_path_only__" in kargs
        try:
            fpath = self._function_names [thing]
            if len (fpath) == 2:
                if not args and not kargs:
                    proto = self.route_map [fpath [0]]['__proto__']
                else:
                    proto = self.route_map_fancy [fpath [0]][fpath [1]]['__proto__']                
            else:    
                proto = self.route_map [fpath [0]]['__proto__']
        except KeyError:
            raise NameError ("{} not found".format (str (thing)))
        func, name, fuvars, favars, numvars, str_rule, options = proto
        
        if script_name_only:
            url = str_rule
            if favars:
                s = url.find ("<")
                if s != -1:
                    url = url [:s]
            return self.urlfor (url)
        
        params = {}
        try:
            currents = kargs.pop ("__defaults__")
        except KeyError:
            currents = {}
        else:
            for k, v in currents.items ():
                if k in fuvars:
                    params [k] = v
        
        if "argspec" in options:
            fuvars, favars, numvars = options ["argspec"]
            if len (args) or favars [0][0] in kargs or favars [0][0] in params:
                n, t = favars[0]
                str_rule += "/<{}{}>".format (t != "string" and (t + ":") or "", favars[0][0])
        
        function_args = options.get ("args", [])
        has_kargs = options.get ("keywords")
        
        for i in range (len (args)):
            try:
                name = function_args [i]
            except IndexError:
                raise ValueError ("too many parameters")
            params [name] = args [i]
        
        for k, v in kargs.items ():
            if not has_kargs and k not in function_args:
                raise ValueError ("parameter {} is not allowed".format (k))
            params [k] = v
        
        url = str_rule
        if favars: #fancy [(name, type),...]. /fancy/<int:cid>/<cname>
            for n, t in favars:
                if n not in params:
                    try:
                        params [n] = currents [n]
                    except KeyError:
                        try:
                            params [n] = options ["defaults"][n]                            
                        except KeyError:
                            raise AssertionError ("Argument '%s' missing" % n)
                     
                value = quote_plus (str (params [n]))
                if t == "string":
                    value = value.replace ("+", "_")
                elif t == "path":
                    value = value.replace ("%2F", "/")
                url = url.replace ("<%s%s>" % (t != "string" and t + ":" or "", n), value)
                del params [n]
        
        if params:
            url = url + "?" + "&".join (["%s=%s" % (k, quote_plus (str(v))) for k, v in params.items ()])
            
        return self.urlfor (url)
    build_url = urlfor
        
    # Routing ------------------------------------------------------                            
    def route (self, rule, **k):
        def decorator (f):
            self.save_function_spec (f)
            self.add_route (rule, f, **k)
            @wraps(f)
            def wrapper (*args, **kwargs):
                return f (*args, **kwargs)
            self._function_names [id (wrapper)] = self.get_func_id (f)
            return wrapper
        return decorator
            
    def get_route_map (self):
        return self.route_map
    
    def set_route_map (self, route_map):
        self.route_map = route_map
    
    def add_route (self, rule, func, **options):
        if not rule or rule [0] != "/":
            raise AssertionError ("Url rule should be starts with '/'")
        
        func_id = self.get_func_id (func)
        is_alter_routing = id (func) in self._function_names
        
        if not is_alter_routing:
            if not self._started and not self._reloading and func_id in self._function_names and "argspec" not in options:
                self.log ("def {} is already defined. use another name or mount (ns = 'myns')".format (func_id), "warn")
            
            if func_id in self._function_names and "argspec" not in options:
                # reloading, remove old func
                deletable = None
                for k, v in self._function_names.items ():
                    if v == func_id:
                        deletable = k
                        break
                if deletable:
                    del self._function_names [deletable]
        
        mount_prefix = self._mount_option.get ("point")
        if not mount_prefix:            
            mount_prefix = self._mount_option.get ("mount")    
                        
        if mount_prefix:            
            while mount_prefix:
                if mount_prefix [-1] == "/":
                    mount_prefix = mount_prefix [:-1]
                else:
                    break    
            rule = mount_prefix + rule
        
        try:
            fspec = self._function_specs [func_id]
        except KeyError:
            fspec =  inspect.getfullargspec(func)            
            self._function_names [id (func)] = func_id
        
        if not is_alter_routing and fspec.varargs is not None:
            raise ValueError ("var args is not allowed")
                            
        options ["args"] = fspec.args [1:]
        options ["keywords"] = fspec.varkw
        
        if fspec.defaults:
            defaults = {}
            argnames = fspec.args[(len (fspec.args) - len (fspec.defaults)):]
            for i in range (len (fspec.defaults)):
                defaults [argnames [i]] = fspec.defaults[i]
            options ["defaults"] = defaults
        
        if self._mount_option.get ("authenticate"):
            options ["authenticate"] = self._mount_option ["authenticate"]
        if self._need_authenticate:
            if func.__name__ == self._need_authenticate [0]:
                options ["authenticate"] = self._need_authenticate [1]
            self._need_authenticate = None        
        # for backward competable    
        if options.get ("authenticate") in (True, 1):
            options ["authenticate"] = self.authenticate or "digest"
        elif options.get ("authenticate") in (False, 0):
            options ["authenticate"] = None
        assert options.get ("authenticate") in self.AUTH_TYPES
         
        s = rule.find ("/<")
        if s == -1:
            s_rule = rule
            try: 
                self.route_map [rule]["__default__"]
            except KeyError:
                pass
            else:
                # IMP: automatically added, but current has priority
                del self.route_map [rule]["__default__"]
            self._function_names [func_id] = (rule,)
            if rule not in self.route_map:
                self.route_map [rule] = {}
            resource = self.route_map [rule]
            proto = (func, func.__name__, func.__code__.co_varnames [1:func.__code__.co_argcount], None, func.__code__.co_argcount - 1, rule, options)

        else:
            prefix = rule [:s]
            s_rule = rule
            rulenames = []
            urlargs = RX_RULE.findall (rule)
            options ["urlargs"] = len (urlargs)
            for r, n in urlargs:
                if n.startswith ("int:"):
                    rulenames.append ((n[4:], n[:3]))
                    rule = rule.replace (r, "/([0-9]+)")
                elif n.startswith ("float:"):
                    rulenames.append ((n[6:], n [:5]))
                    rule = rule.replace (r, "/([.0-9]+)")
                elif n.startswith ("path:"):
                    rulenames.append ((n[5:], n [:4]))
                    rule = rule.replace (r, "/(.+)")    
                else:
                    rulenames.append ((n, "string"))
                    rule = rule.replace (r, "/([^/]+)")
            rule = "^" + rule + "$"            
            re_rule = re.compile (rule)
            self._function_names [func_id] = (prefix, re_rule)
            
            if prefix not in self.route_map_fancy:
                self.route_map_fancy [prefix] = {}
            if re_rule not in self.route_map_fancy [prefix]:    
                self.route_map_fancy [prefix][re_rule] = {}
                
            resource = self.route_map_fancy [prefix][re_rule]            
            proto = (func, func.__name__, func.__code__.co_varnames [1:func.__code__.co_argcount], tuple (rulenames), func.__code__.co_argcount - 1, s_rule, options)
            
            if s > 0 and len (rulenames) == 1 and s_rule [-1] == ">" and rulenames [0][0] in options.get ("defaults", {}):
                simple_rule = s_rule [:s]
                if simple_rule not in self.route_map:    
                    options_ = copy.copy (options)
                    options_ ["argspec"] = proto [2:5]
                    self.add_route (simple_rule, func, **options_)
            
            self._route_priority.append ((prefix, re_rule))
            self._route_priority.sort (key = lambda x: len (x [0]), reverse = True)
        
        
        if "__proto__" in resource:
            methods = set (resource ["__proto__"][-1].get ("methods", []))
        else:
            methods = set (options.get ("methods", []))
            if not methods:
                methods = {"GET", "POST"}
            
        resource ["__proto__"] = proto
        resource ["__default__"] = proto
        for method in options.get ("methods", methods):
            resource [method] = proto
            methods.add (method)
        
        for proto in resource.values ():
            proto [-1]["methods"] = methods
                    
    def get_routed (self, method_chain):
        if not method_chain: 
            return
        temp = method_chain
        while 1:
            routed = temp [1]
            if type (routed) is not list:
                return routed
            temp = routed
                    
    def find_route (self, path_info, command):
        if not path_info:
            return self.urlfor ("/"), None
        if path_info in self.route_map:
            #command = command in self.route_map [path_info] and command or "__default__"            
            try: 
                proto = self.route_map [path_info][command]
            except KeyError:
                raise AssertionError            
            return proto [0], proto [-1]
        
        trydir = path_info + "/"
        if trydir in self.route_map:
            return self.urlfor (trydir), None
        raise KeyError
    
    def verify_rule (self, path_info, rule, protos, command):
        arglist = rule.findall (path_info)
        if not arglist:
            return None, None, None
        
        try:
            f, n, l, a, c, s, options = protos [command]
        except KeyError:
            raise AssertionError
        
        arglist = arglist [0]
        if type (arglist) is not tuple:
            arglist = (arglist,)
            
        kargs = {}
        for i in range (len(arglist)):
            an, at = a [i]
            if at == "int":
                kargs [an] = int (arglist [i])
            elif at == "float":
                kargs [an] = float (arglist [i])
            elif at == "path":
                kargs [an] = unquote_plus (arglist [i])
            else:        
                kargs [an] = unquote_plus (arglist [i]).replace ("_", " ")
                
        return f, options, kargs

    def find_method (self, path_info, command):
        if not (path_info.startswith (self.mount_p) or (path_info + "/").startswith (self.mount_p)):
            return self, None, None, None, 404
        
        path_info = path_info [self.path_suffix_len:]
        method, kargs = None, {}
        
        try:
            try:
                method, options = self.find_route (path_info, command)        
            except KeyError:
                for prefix, rule in self._route_priority:
                    if not path_info.startswith (prefix):
                        continue                    
                    protos = self.route_map_fancy [prefix][rule]
                    method, options, kargs = self.verify_rule (path_info, rule, protos, command)
                    if method:
                        break
        except AssertionError:
            return self, None, None, None, 405 # method not allowed     
                
        if method is None:
            return self, None, None, None, 404
        if isinstance (method, str):
            return self, method, None, None, 301
          
        return (
            self, 
            [self._binds_request [0], method] + self._binds_request [1:4], 
            kargs, 
            options, 
            None
        ) 
    
    # model signal ---------------------------------------------
    def _model_changed (self, sender, **karg):
        model_name = str (sender)[8:-2]
        karg ['x_model_class'] = model_name
        if 'created' not in karg:
            karg ["x_operation"] = 'D'
        elif karg["created"]:
            karg ["x_operation"] = 'C'
        else:
            karg ["x_operation"] = 'U'
        karg ["x_ignore"]    = True
        the_was._get ().setlu (model_name, sender, **karg)
    
    def redirect_signal (self, framework = "django"):
        if framework == "django":    
            from django.db.models.signals import post_save, post_delete        
            post_save.connect (self._model_changed)
            post_delete.connect (self._model_changed)
    model_signal = redirect_signal
    
    # app startup and shutdown --------------------------------------------    
    def cleanup (self):   
        pass
            
    def _start (self, wasc, route, reload = False):
        self.wasc = wasc
        if not route:
            self.basepath = "/"
        elif not route.endswith ("/"):            
            self.basepath = route + "/"
        else:
            self.basepath = route
        
    def start (self, wasc, route):
        self.bus.emit ("app:starting", wasc)
        self._start (wasc, route)
        self.bus.emit ("app:started", wasc)
        self._started = True
        
    def restart (self, wasc, route):        
        self._reloading = True
        self.bus.emit ("app:restarting", wasc)    
        self._start (wasc, route, True)
        self.bus.emit ("app:restarted", wasc)    
        self._reloading = False
    
    #----------------------------------------------
    
    def on (self, *events):
        def decorator(f):            
            self.save_function_spec (f)
            for e in events:
                if self._reloading:
                    try: self.bus.remove_event (f.__name__, e)
                    except EventDoesntExist: pass                
                self.bus.add_event (f, e)
                
            @wraps(f)
            def wrapper(*args, **kwargs):
                return f (*args, **kwargs)
            return wrapper
        return decorator
        
    def emit_after (self, event):
        def outer (f):
            self.save_function_spec (f)
            @wraps (f)
            def wrapper(*args, **kwargs):
                returned = f (*args, **kwargs)
                self.emit (event)
                return returned
            return wrapper
        return outer
            
    def emit (self, event, *args, **kargs):
        self.bus.emit (event, the_was._get (), *args, **kargs)
    
    #-----------------------------------------------
    
    def on_broadcast (self, *events):
        def decorator(f):
            self.save_function_spec (f)
            for e in events:                
                self.add_event (e, f)
            @wraps(f)
            def wrapper(*args, **kwargs):
                return f (*args, **kwargs)
            return wrapper
        return decorator
    # this is for model signal
    on_signal = on_broadcast
         
    def broadcast_after (self, event):
        def decorator (f):
            self.save_function_spec (f)
            @wraps (f)
            def wrapper(*args, **kwargs):
                returned = f (*args, **kwargs)
                the_was._get ().apps.emit (event)
                return returned
            return wrapper
        return decorator
        
    def add_event (self, event, f):
        try:
            del self.events [(f.__name__, event)]
        except KeyError:
            pass
        self.events [(f.__name__, event)] = f
    
    def commit_events_to (self, broad_bus):
        for (fname, event), f in self.events.items ():
            broad_bus.add_event (f, event)
            
    def remove_events (self, broad_bus):
        for (fname, event), f in self.events.items ():
            try:    
                broad_bus.remove_event (fname, event)
            except EventDoesntExist: 
                pass
                   
    # Deprecated -----------------------------------------------    
    @deco.deprecated
    def reload_package (self):
        importer.reloader (self.module)
        self.update_file_info ()
    
    @deco.deprecated
    def reloadable (self):
        if self.module is None: return False
        stat = os.stat (self.abspath)
        return self.file_info != (stat.st_mtime, stat.st_size)
       
       