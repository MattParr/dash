#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, os.path, sys, logging, uuid, datetime, json, random, time

sys.path.append('lib')

from config import settings
from miniredis.client import RedisClient

log = logging.getLogger()

r = RedisClient(**settings.redis)

random.seed(time.time())

def inject():
    event = {
        'id': str(uuid.uuid4()),
        'kittens': str(random.randint(0,70))
    }

    r.setex("event:%s" % event['id'], 60, json.dumps(event))

    clients = r.lrange("dash:clients", 0, -1)
    for client_id in clients:
        r.rpush(client_id, event['id'])

inject()
