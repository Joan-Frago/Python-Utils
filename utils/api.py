import os
import sys

from typing import Callable, List, Tuple
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

import atexit
import json

sys.path.append("/opt/dev/Python-Utils/utils")
from utils import Logger,Timer

class Api:
    def __init__(self,Port:int=8000,logger: Logger = None,init_message:str=None,exit_message:str=None,allowed_origins:List[str]=None):
        self.iPort = Port
        self.routes: List[Tuple[str,Callable]] = []
        self.logger = Logger.get_logger_type(aLogger=logger)
        self.init_message = init_message
        self.exit_message = exit_message
        self.allowed_origins = allowed_origins or ["*"] # Default to allow all origins

        if self.init_message is not None:
            self.logger.info(init_message)
        # Init timer
        self.timer = Timer()
        atexit.register(self.atexit_register)

    def atexit_register(self):
        if self.exit_message is not None:
            exc_time = self.timer.stop()
            self.logger.info(self.exit_message)
            self.logger.info(f"Execution time: {exc_time}")

    def add_cors_headers(self,handler):
        try:
            origin = handler.request.headers.get("Origin",None)
            if "*" in self.allowed_origins or (origin and origin in self.allowed_origins):
                handler.set_header("Access-Control-Allow-Origin", origin if origin else "*")
                handler.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                handler.set_header("Access-Control-Allow-Headers", "Content-Type")
                handler.set_header("Access-Control-Allow-Credentials", "true")

                return True
            else:
                self.logger.info(f"Origin '{origin}' not allowed")
                return False
        except Exception as e:
            self.logger.error(f"Error in add_cors_headers: {e}")

    def add_get_request(self, path:str, handler_function:Callable):
        _logger = self.logger
        class DynamicHandler(RequestHandler):
            def set_default_headers(self):
                if not self.application.api.add_cors_headers(self):
                    self.stop_processing=True
            def prepare(self):
                if getattr(self,"stop_processing",False):
                    self.set_status(403)
                    self.write({"error":"Origin not allowed"})
                    self.finish()
            def get(self):
                try:
                    response=handler_function()
                    self.write(response)
                    # _logger.info(f"request on {handler_function.__name__}")

                except Exception as e:
                    _logger.error("Can't add request: {}".format(e))
            
            def options(self, **kwargs):
                self.application.api.add_cors_headers(self)
                self.set_status(204)
                self.finish()
                    
        self.routes.append((path,DynamicHandler))
    
    def add_post_request(self, path:str, handler_function:Callable):
        _logger = self.logger
        class DynamicHandler(RequestHandler):
            def set_default_headers(self):
                if not self.application.api.add_cors_headers(self):
                    self.stop_processing=True
            def prepare(self):
                if getattr(self,"stop_processing",False):
                    self.set_status(403)
                    self.write({"error":"Origin not allowed"})
                    self.finish()
            def post(self, **kwargs):
                try:
                    # Extract json body, if any, and url params
                    body = self.request.body.decode("utf-8")
                    json_body = self.request.headers.get("Content-Type") == "application/json"
                    data = body if not json_body else json.loads(body)

                    # call handler func with url params and body
                    iRet = handler_function(data, **kwargs)
                    if iRet is None:
                        err="iRet is None in "+self.post.__name__+" function. " + str(sys.exc_info())
                        _logger.error(err)
                        raise Exception(err)
                    if not isinstance(iRet,(str,bytes,dict)):
                        iRet=json.loads(iRet)
                    self.write(iRet)
                
                except Exception as e:
                    err = "Error in post handler : " + str(sys.exc_info()) + " : " + str(e)
                    _logger.error(err)
                    self.set_status(500) # Internal server error
                    self.write({"error": str(e)})
            
            def options(self, **kwargs):
                self.application.api.add_cors_headers(self)
                self.set_status(204)
                self.finish()
        
        self.routes.append((path, DynamicHandler))

    def init_app(self):
        try:
            app = Application(self.routes)
            app.api = self
            app.listen(port=self.iPort)
            IOLoop.instance().start()
        except KeyboardInterrupt:
            sys.exit("\n")
