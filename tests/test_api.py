#!/opt/dev/Python-Utils/tests/venv310/bin/python

import os
import sys

sys.path.append("/opt/dev/Python-Utils/utils")
from utils import *
from api import Api

_logger = Logger("/opt/dev/Python-Utils/tests/test_log.log")

CONSOLE=True


if CONSOLE:
    app = Api(Port=8800,init_message="Started test api",exit_message="Closed test api")
else:
    app = Api(Port=8800,logger=_logger,init_message="Started test api",exit_message="Closed test api")

def test():
    return {"message":"it works"}
def test_post(data, id):
    return {"id": id, "state":"active", "data":data}

app.add_get_request("/test", test)
app.add_post_request(r"/api/testPost/(?P<id>[0-9]+)", test_post)
app.init_app()
