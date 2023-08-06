import zlib
import time
import os
import sys
from aquests.protocols.http import http_date, http_util
from rs4.reraise import reraise 
from rs4 import producers, compressors
from aquests.protocols.http import respcodes
from skitai.wastuff.api import API, catch
import skitai
import asyncore
import json
from skitai import exceptions, http_response
from skitai.handlers.http2 import response as http2_response 

try: 
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin    

class http_response (http_response.http_response):
    def adaptive_error (self, status, message, code, more_info):
        ac = self.request.get_header ('accept', '')
        if ac.find ("text/html") != -1:
            return self.with_explain (status, "{} (code: {}): {}".format (message, code, more_info))
        return self.Fault (sttus, status, message, code, None, more_info)
    
    def fault (self, message = "", code = 0,  debug = None, more_info = None, exc_info = None, traceback = False):
        api = self.api ()
        if not code:
            code = int (self.reply_code) * 100 + (traceback and 90 or 0)
        if traceback:
            api.traceback (message, code, debug or "see traceback", more_info)
        else:    
            api.error (message, code, debug, more_info, exc_info)
        self.update ("Content-Type", api.get_content_type ())            
        return api
    eapi = fault # will be derecating
    
    def throw (self, status, why = ""):
        raise exceptions.HTTPError (status, why)
    
    def with_explain (self, status = "200 OK", why = "", headers = None):
        self.start_response (status, headers)
        return self.build_error_template (why)
    
    # API methods ------------------------------------------------------------
    def API (self, __data_dict__ = None, **kargs):
        if isinstance (__data_dict__, str):
            self.set_status (__data_dict__)
            __data_dict__ = None
        api = API (self.request, __data_dict__ or kargs)
        self.update ("Content-Type", api.get_content_type ())
        return api
    api = API
        
    def Fault (self, status = "200 OK", *args, **kargs):
        self.set_status (status)
        r = self.fault (*args, **kargs)        
        return self (status, r)
    for_api = Fault
    
    def File (self, path, mimetype = 'application/octet-stream', filename = None):
        self.set_header ('Content-Type',  mimetype)
        self.set_header ('Content-Length', str (os.path.getsize (path)))
        if filename:
            self.set_header ('Content-Disposition', 'attachment; filename="{}"'.format (filename))
        return producers.file_producer (open (path, "rb"))                    
    file = File
    
