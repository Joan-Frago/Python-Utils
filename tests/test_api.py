#!/opt/dev/Python-Utils/tests/venv310/bin/python

import os
import sys

sys.path.append("/opt/dev/Python-Utils/utils")
from utils import *
from api import Api

_logger = Logger("/opt/dev/Python-Utils/tests/test_log.log")

def test():
    return {"message":"it works"}

_api = Api(Port=8800,logger=_logger,init_message="Started test api",exit_message="Closed test api")
# _api = Api(Port=8800,init_message="Started test api",exit_message="Closed test api")
_api.add_get_request("/test", test)
_api.init_app()
