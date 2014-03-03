#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, logging, time, uuid, datetime, json, random, itertools

from miniredis.client import RedisClient

log = logging.getLogger()

class EventController:
    """ Uses simple Redis lists to build a broadcast event mechanism. 
        Since we're not using persistent connections, PubSub isn't an option. """
    
    def __init__(self, settings):
        self.redis = RedisClient(**settings.redis)
        self.client_timeout = 120
        self.event_timeout = 60
        random.seed()


    def add_client(self, client_id):
        self.redis.hset("dash:clients", client_id, time.time())
        # create a new initialization event
        self.redis.setex("event:%s" % client_id, self.event_timeout,
                         json.dumps({'event': 'client-id', 'data': client_id}))
        # ...and add a reference to it to a new client queue
        self.redis.rpush("client:%s" % client_id, client_id)


    def del_client(self, client_id):
        return self.redis.hdel("dash:clients", client_id)


    def client_alive(self, client_id):
        self.redis.hset("dash:clients", client_id, time.time())
        return self.redis.expire("client:%s" % client_id, self.client_timeout)


    def expire_clients(self):
        i = iter(self.redis.hgetall("dash:clients"))
        clients = dict(itertools.izip(i,i))
        now = time.time()
        for k in clients.keys():
            if float(clients[k]) < (now - self.client_timeout):
                self.redis.hdel("dash:clients", k)
                self.redis.delete("client:%s" % k)


    def add_event(self, event_name, event_data):
        if not random.randint(0,3):
            self.expire_clients()
        event_id = str(uuid.uuid4())
        # store the event data
        self.redis.setex("event:%s" % event_id,
                         self.event_timeout,
                         json.dumps({
                             'event': event_name,
                             'data' : event_data
                         }))
        # propagate it to all clients
        clients = self.redis.hkeys("dash:clients")
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

            try:
                event = json.loads(buf)
                event.update({'id': event_id})
                yield event
            except Exception as e:
                log.warn("Could not parse '%s' as JSON" % buf)
                break
