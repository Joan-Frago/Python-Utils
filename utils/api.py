import os
import sys

from typing import Callable, List, Tuple
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

import atexit

sys.path.append("/opt/dev/Python-Utils/utils")
from utils import Logger,Timer

class Api:
    def __init__(self,Port:int=8000,logger: Logger = None,init_message:str=None,exit_message:str=None):
        self.iPort = Port
        self.routes: List[Tuple[str,Callable]] = []
        self.logger = Logger.get_logger_type(aLogger=logger)
        self.init_message = init_message
        self.exit_message = exit_message

        if self.init_message is not None:
            self.logger.info(init_message)
        # Init timer
        self.timer = Timer()
        atexit.register(self.atexit_register)

    def atexit_register(self):
        if self.exit_message is not None:
            exc_time = self.timer.stop()
            self.logger.info("Closed program")
            self.logger.debug(f"Execution time: {exc_time}")
    
    def add_get_request(self, path:str, handler_function:Callable):
        _logger = self.logger
        class DynamicHandler(RequestHandler):
            def get(self):
                try:
                    response=handler_function()
                    self.write(response)
                    _logger.info(f"request on {handler_function.__name__}")

                except Exception as e:
                    _logger.error("Can't add request: {}".format(e))
                    
        self.routes.append((path,DynamicHandler))

    def init_app(self):
        try:
            app = Application(self.routes)
            app.listen(port=self.iPort)
            IOLoop.instance().start()
        except KeyboardInterrupt:
            pass
