# -*- coding: utf-8 -*-
from logzero import logger

from chaoslib.types import Configuration
from sky_wiremock.sky_wiremock import Wiremock
from .utils import get_wm_server, check_configuration

__all__ = [
        "mappings"
]


def mappings(c: Configuration={}):
    if (not check_configuration(c)):
        return []
    w = Wiremock(url = get_wm_server(c))
    return w.mappings()
