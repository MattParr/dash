#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, os.path, sys, logging, uuid, datetime, json
from bottle import app, request, response, route, redirect, static_file, view

from utils import path_for
from config import settings
from controllers.events import EventController

log = logging.getLogger()

c = EventController(settings)

def pack(d):
    buffer = ''
    for k in ['retry','id','event','data']:
        if k in d.keys():
            buffer += '%s: %s\n' % (k, d[k])
    return buffer + '\n'


@route('/event')
def event():
    client_id = request.get_cookie("client-id")
    if not (client_id and c.client_alive(client_id)):
        client_id = str(uuid.uuid4())
        response.set_cookie("client-id", client_id)
        c.add_client(client_id)

    # now fetch all the events this client is entitled to
    buffer = pack({
        'retry': '5000',
        'id'   : uuid.uuid4(),
        'event': 'tick',
        'data' : str(datetime.datetime.now())
    })
    for e in c.get_events_for_client(client_id):
        buffer += pack(e)

    #log.debug(map(lambda x: (x,request.headers[x]),request.headers.keys()))
    log.debug(dict(request.headers))
    log.debug("Pack: %s" % buffer)
    response.headers['content-type'] = 'text/event-stream'
    return buffer
