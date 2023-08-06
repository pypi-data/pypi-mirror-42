#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest


from chaoswm.actions import \
    add_mappings,           \
    delete_mappings,        \
    global_fixed_delay,     \
    global_random_delay,    \
    fixed_delay,            \
    random_delay,           \
    chunked_dribble_delay,  \
    down,                   \
    up,                     \
    reset

from chaoswm.probes import  \
    mappings

from chaoswm.utils import can_connect_to, get_wm_server

from http.client import HTTPConnection
import logging
HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


@unittest.skipIf(can_connect_to("localhost", 8080) is False, "Test skipped: wiremock server not running")
class TestActions( unittest.TestCase ):

    def test_wm_server_void_config(self):
        url = get_wm_server({})
        self.assertIsNone(url)


    def text_wm_server_host_and_port(self):
        url = get_wm_server({
            "wiremock":{
                "host":"localhost",
                "port":8080
            }
        })
        self.assertEqual(url, "http://localhost:8080")

    def test_wm_server_url(self):
        url = get_wm_server({
            "wiremock":{
                "url":"http://localhost:8080/"
            }
        })
        self.assertEqual(url, "http://localhost:8080/")

    def test_global_fixed_delay(self):
        self.assertEqual(global_fixed_delay(
            10,
            {
                "wiremock":{
                    "host":"localhost",
                    "port": 8080,
                }
            }), 1)


    def test_global_random_delay(self):
        self.assertEqual(global_random_delay(
            {
                "type": "lognormal",
                "median": 20,
                "sigma": 0.1
            },
            {
                "wiremock":{
                    "host":"localhost",
                    "port": 8080,
                }
            }), 1)


    def test_add_mappings(self):
#         import pdb; pdb.set_trace()
        ids = add_mappings([{
            "request": {
                "method": "GET",
                "url": "/some/thing"
            },
            "response": {
                "status": 200,
                "body": "Hello world!",
                "headers": {
                    "Content-Type": "text/plain"
                }
            } 
        }],
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080,
           },
        })

        delete_mappings([{
                "url":"/some/thing", 
                "method":"GET"
            }],
            {
                "wiremock":{
                   "host":"localhost",
                   "port": 8080,
              }
            })

        self.assertTrue(isinstance(ids[0], str))
        self.assertTrue(ids[0] != -1)


    def test_delete_mappings(self):
        self.assertEqual(reset(
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080
           },
        }), 1)
        ids_added=add_mappings([{
            "request": {
                "method": "GET",
                "url": "/some/thing"
            },
            "response": {
                "status": 200,
                "body": "Hello world!",
                "headers": {
                    "Content-Type": "text/plain"
                }
            } 
        }],
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080
           },
        })
        ids_deleted=delete_mappings([{
                "url":"/some/thing", 
                "method":"GET"
            }],
            {
                "wiremock":{
                   "host":"localhost",
                   "port": 8080
              }
            }
        )
        self.assertTrue(isinstance(ids_deleted[0], str))
        self.assertEqual(ids_added[0], ids_deleted[0])


    def test_fixed_delay(self):
        self.assertEqual(reset(
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080
           },
        }), 1)
        ids_added=add_mappings([{
            "request": {
                "method": "GET",
                "url": "/some/thing"
            },
            "response": {
                "status": 200,
                "body": "Hello world!",
                "headers": {
                    "Content-Type": "text/plain"
                }
            } 
        }],
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080
           },
        })
        self.assertEqual(fixed_delay(
            filter=[{
                "url":"/some/thing",
                "method":"GET"
            }],
            fixedDelayMilliseconds=10,
            configuration={
               "wiremock":{
                   "host":"localhost",
                   "port": 8080
               },
            }), ids_added)
        ids_deleted=delete_mappings([{
                "url":"/some/thing", 
                "method":"GET"
            }],
            {
                "wiremock":{
                   "host":"localhost",
                   "port": 8080
              }
            }
        )
        self.assertTrue(isinstance(ids_deleted[0], str))
        self.assertEqual(ids_added[0], ids_deleted[0])


    def test_random_delay(self):
        self.assertEqual(reset(
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080
           },
        }), 1)
        ids_added=add_mappings([{
            "request": {
                "method": "GET",
                "url": "/some/thing"
            },
            "response": {
                "status": 200,
                "body": "Hello world!",
                "headers": {
                    "Content-Type": "text/plain"
                }
            } 
        }],
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080
           },
        })
        self.assertEqual(random_delay(
            filter=[{
                "url":"/some/thing",
                "method":"GET"
            }],
            delayDistribution={
                "type": "lognormal",
                "median": 80,
                "sigma": 0.4
            },
            configuration={
               "wiremock":{
                   "host":"localhost",
                   "port": 8080
               },
            }), ids_added)
        ids_deleted=delete_mappings([{
                "url":"/some/thing", 
                "method":"GET"
            }],
            {
                "wiremock":{
                   "host":"localhost",
                   "port": 8080
              }
            }
        )
        self.assertTrue(isinstance(ids_deleted[0], str))
        self.assertEqual(ids_added[0], ids_deleted[0])


    def test_chunked_dribble_delay(self):
        self.assertEqual(reset(
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080
           },
        }), 1)
        ids_added=add_mappings([{
            "request": {
                "method": "GET",
                "url": "/some/thing"
            },
            "response": {
                "status": 200,
                "body": "Hello world!",
                "headers": {
                    "Content-Type": "text/plain"
                }
            } 
        }],
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080
           },
        })
        self.assertEqual(chunked_dribble_delay(
            filter=[{
                "url":"/some/thing",
                "method":"GET"
            }],
            chunkedDribbleDelay={
                "numberOfChunks": 5,
                "totalDuration": 1000
            },
            configuration={
               "wiremock":{
                   "host":"localhost",
                   "port": 8080
               },
            }), ids_added)
        ids_deleted=delete_mappings([{
                "url":"/some/thing", 
                "method":"GET"
            }],
            {
                "wiremock":{
                   "host":"localhost",
                   "port": 8080
              }
            }
        )
        self.assertTrue(isinstance(ids_deleted[0], str))
        self.assertEqual(ids_added[0], ids_deleted[0])


    def test_down(self):
        self.assertEqual(reset(
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080
           },
        }), 1)
        ids_added=add_mappings([{
            "request": {
                "method": "GET",
                "url": "/some/thing"
            },
            "response": {
                "status": 200,
                "body": "Hello world!",
                "headers": {
                    "Content-Type": "text/plain"
                }
            } 
        }],
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080
           },
        })
        self.assertEqual(down(
            filter=[{
                "method": "GET",
                "url": "/some/thing"
            }],
            configuration={
                "wiremock":{
                    "host":"localhost",
                    "port": 8080,
                    "defaults": {
                        "down": {
                            "numberOfChunks": 10,
                            "totalDuration": 4000
                        }
                    }
                },
            }), ids_added)


    def test_down(self):
        self.assertEqual(reset(
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080
           },
        }), 1)
        ids_added=add_mappings([{
            "request": {
                "method": "GET",
                "url": "/some/thing"
            },
            "response": {
                "status": 200,
                "body": "Hello world!",
                "headers": {
                    "Content-Type": "text/plain"
                }
            } 
        }],
        {
           "wiremock":{
               "host":"localhost",
               "port": 8080
           },
        })
        self.assertEqual(down(
            filter=[{
                "method": "GET",
                "url": "/some/thing"
            }],
            configuration={
                "wiremock":{
                    "host":"localhost",
                    "port": 8080,
                    "defaults": {
                        "down": {
                            "numberOfChunks": 10,
                            "totalDuration": 4000
                        }
                    }
                },
            }), ids_added)

        reset_ids = up([{
            "method": "GET",
            "url": "/some/thing"
            }],
            {
                "wiremock":{
                    "host":"localhost",
                    "port": 8080
                }
            })
        m = mappings({
            "wiremock":{
                "host":"localhost",
                "port": 8080
            }
        })
        self.assertTrue("chunkedDribbleDelay" not in m[0]["response"])
