#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, os.path, sys, logging, uuid, datetime, json, random, time

sys.path.append('lib')

from config import settings
from controllers.events import EventController

log = logging.getLogger()

c = EventController(settings)

random.seed(time.time())

for i in range(0,4):
    c.add_event('kitten-count', str(random.randint(0,70)))
    time.sleep(10)
