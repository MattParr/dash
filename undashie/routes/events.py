#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, os.path, sys, logging, uuid, datetime
from bottle import app, request, response, route, redirect, static_file, view

from utils import path_for
from config import settings

log = logging.getLogger()


def pack(d):
    buffer = ''
    for k in ['retry','id','event','data']:
        if k in d.keys():
            buffer += '%s: %s\n' % (k, d[k])
    return buffer + '\n'


@route('/event')
def event():
    if not request.get_cookie("client-id"):
        response.set_cookie("client-id", str(uuid.uuid4()))

    log.debug(map(lambda x: (x,request.headers[x]),request.headers.keys()))
    response.headers['content-type'] = 'text/event-stream'
    msg = {
        'retry': '5000',
        'event': 'tick',
        'data': str(datetime.datetime.now()),
    }

    if 'Last-Event-Id' in request.headers:
        msg['id'] = str(int(request.headers['Last-Event-Id']) + 1)
    else:
        msg['id'] = "0"

    buffer = pack(msg)
    print buffer
    return buffer