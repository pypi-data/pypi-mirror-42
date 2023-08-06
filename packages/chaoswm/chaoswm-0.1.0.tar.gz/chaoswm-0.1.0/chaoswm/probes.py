# -*- coding: utf-8 -*-
from logzero import logger

from chaoslib.types import Configuration
from sky_wiremock.sky_wiremock import Wiremock, ConnectionError
from .utils import get_wm_server, check_configuration

__all__ = [
        "mappings",
        "server_running"
]


def server_running(c: Configuration={}):
    if (not check_configuration(c)):
        return []
    try:
        w = Wiremock(url = get_wm_server(c))
        return 1
    except ConnectionError:
        logger.error("Error: Wiremock server not running")
        return 0


def mappings(configuration: Configuration={}):
    if (not check_configuration(configuration)):
        return []
    try:
        w = Wiremock(url = get_wm_server(configuration))
        return w.mappings()
    except ConnectionError:
        logger.error("Error connecting to Wiremock server")
        return None

