import socket
from logzero import logger

from contextlib import closing


def can_connect_to(host, port):
    """ Test a connection to a host/port """

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return bool(sock.connect_ex((host, port)) == 0)


def get_wm_server(c: dict):
    wm_conf = c.get("wiremock", {})

    url  = wm_conf.get("url",  None)
    host = wm_conf.get("host", None)
    port = wm_conf.get("port", None)

    if (host and port and not url):
        url = "http://{}:{}".format(host,port)
    
    if (not url):
        logger.error("ERROR: no configuration params to set WM server url")
        return None

    return url


def check_configuration(c: dict={}):
    if ("wiremock" not in c):
        logger.error("Error: wiremock key not found in configuration section")
        return -1
    return 1
