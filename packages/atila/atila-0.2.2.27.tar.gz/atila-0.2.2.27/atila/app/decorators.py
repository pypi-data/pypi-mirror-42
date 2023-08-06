from functools import wraps
import os
import copy
from skitai import was as the_was
import time, threading
from event_bus.exceptions import EventDoesntExist
from rs4 import evbus
import time
import re
import inspect

RX_RULE = re.compile ("(/<(.+?)>)")

class Decorators:    
    def __init__ (self):        
        self.bus = evbus.EventBus ()
        
        self.route_map = {}
        self.route_map_fancy = {}        
        self.events = {}        
        self.handlers = {}
        
        self._ws_channels = {}
        self._maintern_funcs = {}        
        self._mount_option = {}        
        self._decos = {
            "bearer_handler": self.default_bearer_handler
        }
        self._reloading = False        
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

    # function param saver ------------------------------------------
    def get_func_id (self,  func):
        return ("ns" in self._mount_option and self._mount_option ["ns"] + "." or "") + func.__name__
    
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
    RX_EMAIL = re.compile (r"[a-z0-9][-.a-z0-9]*@[-a-z0-9]+\.[-.a-z0-9]{2,}", re.I)
    RX_UUID = re.compile (r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
    def _validate_param (self, params, required, ints, floats, emails, uuids, **kargs):
        params = params or {}
        if required:
            for each in required:
                if not params.get (each):
                    return 'parameter {} required'.format (each)                                                
        if ints:
            for each in ints:
                try: int (params [each])
                except ValueError:
                    return 'parameter {} should be integer'.format (each)                                   
        if floats:
            for each in floats:
                try: float (params [each])
                except ValueError:
                    return 'parameter {} should be float'.format (each)                    
        if emails:
            for fd in emails:
                kargs [fd] = self.RX_EMAIL
        if uuids:
            for fd in uuids:
                kargs [fd] = self.RX_UUID

        for fd_, cond in kargs.items ():
            ops = fd_.split ("__")
            fd = ops [0]
            val = params.get (fd)
            if not val:
                continue
            assert len (ops) <= 3 and fd, "Invalid expression"
            if len (ops) == 1:
                if hasattr (cond, "search"):
                    if not cond.search (val):
                        return 'parameter {} is invalid'.format (fd)
                elif val != cond:
                    return 'parameter {} is invalid'.format (fd)
                continue
            
            if len (ops) == 3:
                if ops [1] == "len":
                    val = len (val)
                    fd = "length of {}".format (fd)
                
            op = ops [-1]
            val = (isinstance (cond, (list, tuple)) and type (cond [0]) or type (cond)) (val)                
            if op == "neq":
                if val == cond:
                    return 'parameter {} should be {}'.format (fd, cond)
            elif op == "in":
                if val not in cond:
                    return 'parameter {} should be one of {}'.format (fd, cond)
            elif op == "notin":
                if val in cond:
                    return 'parameter {} should be not one of {}'.format (fd, cond)
            elif op == "between":
                if not (cond [0] <= val <= cond [1]):
                    return 'parameter {} should be between {} ~ {}'.format (fd, cond [0], cond [1])
            elif op == "lte":
                if val > cond:
                    return 'parameter {} should less or equal than {}'.format (fd, cond)
            elif op == "lt":
                if val >= cond:
                    return 'parameter {} should less than {}'.format (fd, cond)
            elif op == "gte":
                if val < cond:
                    return 'parameter {} should greater or equal than {}'.format (fd, cond)
            elif op == "gt":
                if val <= cond:
                    return 'parameter {} should greater than {}'.format (fd, cond)
            else:
                raise ValueError ("Unknown operator: {}".format (op))

    def parameters_required (self, scope, required = None, ints = None, floats = None, emails = None, uuids = None, **kargs):
        def decorator(f):
            self.save_function_spec (f)        
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                more_info = self._validate_param (getattr (was.request, scope), required, ints, floats, emails, uuids, **kargs)
                if more_info:
                    return was.response.adaptive_error ("400 Bad Request", 'missing or bad parameter'.format (scope), 40050, more_info) 
                return f (was, *args, **kwargs)
            return wrapper
        return decorator
    params_required = parameters_required
    
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
            @wraps(f)
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
    def websocket (self, spec, timeout = 60, onopen = None, onclose = None, encoding = "text"):
        def decorator(f):
            self.save_function_spec (f)
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                if not was.wshasevent ():
                    return f (was, *args, **kwargs)
                if was.wsinit ():
                    return was.wsconfig (spec, timeout, encoding)
                elif was.wsopened ():
                    return onopen and onopen (was) or ''
                elif was.wsclosed ():                    
                    return onclose and onclose (was) or ''
            return wrapper
        return decorator
    websocket_config = websocket
    
    def register_websocket (self, client_id, send):
        self._ws_channels [client_id] = send
    
    def remove_websocket (self, client_id):
        try: self._ws_channels [client_id]
        except KeyError: pass
    
    def websocket_send (self, client_id, msg):
        try: 
            self._ws_channels [client_id] (msg)
        except KeyError: 
            pass
    
    # Mainterinancing -------------------------------------------------------
    def maintain (self, f):
        if not self._started:
            assert f.__name__ not in self._maintern_funcs, "maintain func {} is already exists".format (f.__name__)
        self._maintern_funcs [f.__name__] = f
        return f
    
    # Error handling ------------------------------------------------------    
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
            
            if s >= 0 and len (rulenames) == 1 and s_rule [-1] == ">" and rulenames [0][0] in options.get ("defaults", {}):
                simple_rule = s_rule [:s] or "/"                
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
    
    # Events ----------------------------------------------
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
    
    # Broadcating ----------------------------------------
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
            
    