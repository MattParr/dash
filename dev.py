#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: et:ts=4:sw=4:
"""
Main application script

Created by: Rui Carmo
License: MIT (see LICENSE.md for details)
"""

import os, sys, json, logging

# Make sure our bundled libraries take precedence
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'lib'))

import utils, bottle, miniredis.server
from config import settings

log = logging.getLogger()

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

if "BOTTLE_CHILD" not in os.environ:
    try:
        miniredis.server.fork()
    except Exception as e:
        log.debug("Cannot start built-in Redis: %s" % e)

if settings.reloader:
    if "BOTTLE_CHILD" not in os.environ:
        log.debug("Using reloader, spawning first child.")
    else:
        log.debug("Child spawned.")

# Bind routes
if not settings.reloader or ("BOTTLE_CHILD" in os.environ):
    log.info("Setting up application.")
    import routes

if __name__ == "__main__":
    log.info("Serving requests.")
    bottle.run(
        port     = settings.http.port,
        host     = settings.http.bind_address,
        debug    = settings.debug,
        reloader = settings.reloader
    )
else:
    log.info("Running under uWSGI")
    app = bottle.default_app()
