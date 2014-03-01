#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, logging, uuid, datetime, json

from miniredis.client import RedisClient

log = logging.getLogger()


class EventController:
    """ Uses simple Redis lists to build a broadcast event mechanism. 
        Since we're not using persistent connections, PubSub isn't an option. """
    
    def __init__(self, settings):
        self.redis = RedisClient(**settings.redis)


    def add_client(self, client_id):
        self.redis.rpush("dash:clients", client_id)
        # create a new initialization event
        self.redis.setex("event:%s" % client_id, 60,
                         json.dumps({'event': 'client-id', 'data': client_id}))
        # ...and add a reference to it to a new client queue
        self.redis.rpush("client:%s" % client_id, client_id)


    def client_alive(self, client_id):
        return self.redis.expire("client:%s" % client_id, 120)


    def add_event(self, event_name, event_data):
        event_id = str(uuid.uuid4())
        # store the event data
        self.redis.setex("event:%s" % event_id,
                         60,
                         json.dumps({
                             'event': event_name,
                             'data' : event_data
                         }))
        # propagate it to all clients
        clients = self.redis.lrange("dash:clients", 0, -1)
        for client_id in clients:
            self.redis.rpush("client:%s" % client_id, event_id)


    def get_events_for_client(self, client_id):
        for i in xrange(self.redis.llen("client:%s" % client_id)):

            # pop each ID from the queue
            event_id = self.redis.lpop("client:%s" % client_id) 

            if not event_id:
                break

            # grab the corresponding data
            buf = self.redis.get("event:%s" % event_id)

            ev = None
            if not buf:
                break
            try:
                ev = json.loads(buf)
                log.warn(ev)
            except Exception as e:
                log.debug("Could not parse %s" % ev)
                break

            if ev:
                yield ev.update({'id': event_id})
