from functools import wraps
import os


class SessAuth:
    def __init__ (self):
        self._permission_map = {}

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
