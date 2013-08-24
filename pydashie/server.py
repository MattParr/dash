import os
from flask import Flask, render_template, Response, send_from_directory, request, current_app
import glob

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))

@app.route("/")
def main():
    return render_template('main.html', title='pyDashie')

@app.route("/assets/application.js")
def javascripts():
    if not hasattr(current_app, 'javascripts'):
        import coffeescript

        ordered_script_names = [
            'jquery.js',
            'es5-shim.js',
            'd3.v2.min.js',
            'batman.js',
            'batman.jquery.js',
            'jquery.gridster.js',
            'jquery.leanModal.min.js',
            'dashing.gridster.coffee',
            'jquery.knob.js',
            'rickshaw.min.js'
        ]

        scripts = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'javascripts', js) for js in ordered_script_names]
        for ext in ['js', 'coffee']: scripts.extend(glob.glob(os.path.join(os.getcwd(), "assets/**/*.%s") % ext))
        for ext in ['js', 'coffee']: scripts.extend(glob.glob(os.path.join(os.getcwd(), "widgets/**/*.%s") % ext))

        output = []
        for path in scripts:
            output.append('// JS: %s\n' % path)
            if '.coffee' in path:
                print('Compiling Coffee for %s ' % path)
                contents = coffeescript.compile_file(path).encode('ascii','ignore')
            else:
                print('Reading JS for %s ' % path)
                f = open(path)
                contents = f.read()
                f.close()

            output.append(contents)

        current_app.javascripts = "\n".join(output)

    return Response(current_app.javascripts, mimetype='application/javascript')

@app.route('/assets/application.css')
def application_css():
    scripts = [
        os.path.join(os.getcwd(), 'assets/stylesheets/application.css'),
    ]
    output = ''
    for path in scripts:
        output = output + open(path).read()
    return Response(output, mimetype='text/css')

@app.route('/assets/images/<path:filename>')
def send_static_img(filename):
    directory = os.path.join(os.getcwd(), 'assets', 'images')
    return send_from_directory(directory, filename)

@app.route('/views/<widget_name>.html')
def widget_html(widget_name):
    html = '%s.html' % widget_name
    path = os.path.join(os.getcwd(), 'widgets', widget_name, html)
    if os.path.isfile(path):
        f = open(path)
        contents = f.read()
        f.close()
        return contents

import Queue

class Z:
    pass
xyzzy = Z()
xyzzy.events_queue = {}
xyzzy.last_events = {}
xyzzy.using_events = True
xyzzy.MAX_QUEUE_LENGTH = 20

@app.route('/events')
def events():
    if xyzzy.using_events:
        event_stream_port = request.environ['REMOTE_PORT']
        current_event_queue = Queue.Queue()
        xyzzy.events_queue[event_stream_port] = current_event_queue
        current_app.logger.info('New Client %s connected. Total Clients: %s' %
                                (event_stream_port, len(xyzzy.events_queue)))

        #Start the newly connected client off by pushing the current last events
        for event in xyzzy.last_events.values():
            current_event_queue.put(event)
        return Response(pop_queue(current_event_queue), mimetype='text/event-stream')

    return Response(xyzzy.last_events.values(), mimetype='text/event-stream')

def pop_queue(current_event_queue):
    while True:
        data = current_event_queue.get()
        yield data

def close_stream(*args, **kwargs):
    event_stream_port = args[2][1]
    del xyzzy.events_queue[event_stream_port]
    print('Client %s disconnected. Total Clients: %s' % (event_stream_port, len(xyzzy.events_queue)))
