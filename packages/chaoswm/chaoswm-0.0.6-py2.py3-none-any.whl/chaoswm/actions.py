# -*- coding: utf-8 -*-
from logzero import logger

from chaoslib.types import Configuration
from sky_wiremock.sky_wiremock import Wiremock
from .utils import get_wm_server, check_configuration

__all__ = [
        "add_mappings",
        "delete_mappings",
        "mappings",
        "global_fixed_delay",
        "global_random_delay",
        "fixed_delay"
        "random_delay",
        "chunked_dribble_delay",
        "down",
        "up",
        "reset"
]


def mappings(configuration: Configuration={}):
    if (not check_configuration(configuration)):
        return []
    w = Wiremock(url = get_wm_server(configuration))
    return w.mappings()


def add_mappings(mappings: list=[], configuration: Configuration={}):
    """ adds more mappings to wiremock
    returns the list of ids of the mappings added
    """
    if (not check_configuration(configuration)):
        return []

    w = Wiremock(url = get_wm_server(configuration))
    return w.populate(mappings)

def delete_mappings(filters: list=[], configuration: Configuration={}):
    """ deletes a list of mappings
    returns the list of ids of the mappings deleted
    """
    if (not check_configuration(configuration)):
        return []

    w = Wiremock(url = get_wm_server(configuration))

    ids = []
    for filter in filters:
        if (("url" not in filter) or ("method" not in filter)):
            logger("Filter key url/method missing")
            next
        else:
            url = filter["url"]
            method = filter["method"]
            mapping = w.mapping_by_url_and_method(url=url, method=method)
            if ("id" not in mapping):
                logger.error("Error: mapping {} {} not found".format(method, url))
                next
            else:
                ids.append(w.delete_mapping(mapping["id"]))
    return ids


def down(filter: list=[], configuration: Configuration={}):
    """ set a list of services down
    more correctly it adds a chunked dribble delay to the mapping
    as defined in the configuration section (or action attributes)
    """
    w = Wiremock(url = get_wm_server(configuration))
    conf = configuration.get('wiremock', {})
    if ('defaults' not in conf):
        logger.error("down defaults not specified in config")
        return -1

    defaults = conf.get('defaults',{})
    if ('down' not in defaults):
        logger.error("down defaults not specified in config")
        return -1

    ids = []
    for f in filter:
        ids.append(w.chunked_dribble_delay(f, defaults['down']))
    return ids


def global_fixed_delay(fixedDelay: int=0, configuration: Configuration={}):
    """ add a fixed delay to all mappings """
    w = Wiremock(url = get_wm_server(configuration))
    return w.global_fixed_delay(fixedDelay)


def global_random_delay(delayDistribution: dict={}, configuration: Configuration={}):
    """ adds a random delay to all mappings """
    w = Wiremock(url = get_wm_server(configuration))
    return w.global_random_delay(delayDistribution)

    
def fixed_delay(filter: list=[], fixedDelayMilliseconds: int=0, configuration: Configuration={}):
    """ adds a fixed delay to a list of mappings """
    w = Wiremock(url = get_wm_server(configuration))

    ids=[]
    for f in filter:
        ids.append(w.fixed_delay(f["url"], f["method"], fixedDelayMilliseconds))
    return ids


def random_delay(filter: list=[], delayDistribution: dict={}, configuration: Configuration={}):
    """adds a random delay to a list of mapppings"""
    w = Wiremock(url = get_wm_server(configuration))
    ids=[]
    for f in filter:
        ids.append(w.random_delay(f, delayDistribution))
    return ids


def chunked_dribble_delay(filter: list=[], chunkedDribbleDelay: dict={}, configuration: Configuration={}):
    """adds a chunked dribble delay to a list of mappings"""
    w = Wiremock(url = get_wm_server(configuration))
    ids=[]
    for f in filter:
        ids.append(w.chunked_dribble_delay(f, chunkedDribbleDelay))
    return ids


def up(filter: list=[], configuration: Configuration={}):
    """ deletes all delays connected with a list of mappings """
    w = Wiremock(url = get_wm_server(configuration))
    return w.up(filter)

def reset(configuration: Configuration={}):
    """ resets the wiremock server: deletes all mappings! """
    w = Wiremock(url = get_wm_server(configuration))
    return w.reset()
