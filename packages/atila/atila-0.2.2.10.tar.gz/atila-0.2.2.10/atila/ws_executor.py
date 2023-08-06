from . import wsgi_executor
from aquests.protocols.http import respcodes
from skitai.http_response import catch

class Executor (wsgi_executor.Executor):
	def __call__ (self):
		current_app, wsfunc = self.env.get ("websocket.handler")
		self.was = self.env ["skitai.was"]
		self.was.subapp = current_app		
		try:
			content = wsfunc (self.was, **self.env.get ("websocket.params", {}))			
		except:			
			content = self.was.app.debug and "[ERROR] " + catch (0) or "[ERROR]"
		
		# clean was		
		del self.was.env		
		del self.was.subapp		
		return content
