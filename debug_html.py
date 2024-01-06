from urllib3 import PoolManager, HTTPResponse
from urllib3.exceptions import TimeoutError
from typing import Optional

from prot_http.const_wifi import *
from prot_http.command_http import *

def get_response(http : PoolManager, cmd : YiHttpCmd) -> Optional[bytearray]:
    json = str(cmd.to_json()).replace("'", '"').replace(' "', '"')
    url = "http://%s/?data=%s" % (INET_ADDRESS_CAMERA, json)
    try:
        response : HTTPResponse = http.request("GET", url, timeout=1.0)
        return response.data
    except TimeoutError:
        return None

http = PoolManager()
print(get_response(http, RcCmdStart()))