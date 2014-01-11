#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, os.path, sys, logging, uuid, datetime
from bottle import app, request, response, route, redirect, static_file, view

from utils import path_for
from config import settings
from miniredis.client import RedisClient

log = logging.getLogger()

r = RedisClient(**settings.redis)

def pack(d):
    buffer = ''
    for k in ['retry','id','event','data']:
        if k in d.keys():
            buffer += '%s: %s\n' % (k, d[k])
    return buffer + '\n'


@route('/event')
def event():
    client_id = request.get_cookie("client-id")
    if not client_id:
        client_id = str(uuid.uuid4())
        response.set_cookie("client-id", client_id)
        # add this to the clients list
        r.rpush("dash:clients", client_id)
        # create a new initialization event
        r.setex("event:%s" % client_id, 5, json.dumps({"client-id": client_id}))
        # ...and add a reference to it to a new client queue
        r.rpush("client:%s" % client_id, "event:%s" % client_id)
    # reset the queue timeout
    r.expire("client:%s" % client_id, 120)
    # TODO: remove item from dash:clients if queue expired

    # now fetch all the events this client is entitled to
    events = [{
        'retry': '5000',
        'id'   : uuid.uuid4(),
        'event': 'tick',
        'data' : str(datetime.datetime.now())
    }]
    for i in range(r.llen("client:%s" % client_id))
        # pop each ID from the queue and grab the corresponding data
        event_id = r.lpop("client:%s") 
        if not event_id:
            break
        ev = r.get(event_id)
        if not ev:
            break
        try:
            ev = json.loads(ev)
        except Exception as e:
            log.debug("Could not parse %s" % ev)
            break
        for k in ev.keys:
            events.append({'id': event_id, 'event': k, 'data': json.dumps(ev[k])})

    log.debug(map(lambda x: (x,request.headers[x]),request.headers.keys()))
    response.headers['content-type'] = 'text/event-stream'
    buffer = ''
    for e in events:
        buffer += pack(e)
    return buffer
