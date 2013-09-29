import os

from flask import Response
from flask import current_app
from flask import render_template
from flask import request
from flask import send_from_directory
from scss import Scss
import Queue
import coffeescript
import glob

from pydashie import app
from pydashie import xyzzy


@app.route("/")
def main():
    return render_template("main.html", title="pyDashie")


@app.route("/assets/application.js")
def javascripts():
    if not hasattr(current_app, "javascripts"):

        ordered_script_names = [
            "jquery.js",
            "es5-shim.js",
            "d3.v2.min.js",
            "batman.js",
            "batman.jquery.js",
            "jquery.gridster.js",
            "jquery.leanModal.min.js",
            "dashing.gridster.coffee",
            "jquery.knob.js",
            "rickshaw.min.js"
        ]

        scripts = []
        for js in ordered_script_names:
            script_filename = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "javascripts",
                js
            )
            scripts.append(script_filename)
        for ext in ["js", "coffee"]:
            scripts.extend(
                glob.glob(os.path.join(os.getcwd(), "assets/**/*.%s") % ext)
            )
        for ext in ["js", "coffee"]:
            scripts.extend(
                glob.glob(os.path.join(os.getcwd(), "widgets/**/*.%s") % ext)
            )

        output = []
        for path in scripts:
            output.append("// JS: %s\n" % path)
            if ".coffee" in path:
                print("Compiling Coffee for %s " % path)
                contents = \
                    coffeescript.compile_file(path).encode("ascii", "ignore")
            else:
                print("Reading JS for %s " % path)
                f = open(path)
                contents = f.read()
                f.close()

            output.append(contents)

        current_app.javascripts = "\n".join(output)

    return Response(current_app.javascripts, mimetype="application/javascript")


@app.route("/assets/application.css")
def application_css():
    parser = Scss()

    stylesheets = []
    for ext in ["css", "scss"]:
        stylesheets.extend(
            glob.glob(os.path.join(os.getcwd(), "assets/**/*.%s") % ext)
        )
    for ext in ["css", "scss"]:
        stylesheets.extend(
            glob.glob(os.path.join(os.getcwd(), "widgets/**/*.%s") % ext)
        )

    output = []
    for path in stylesheets:
        if ".scss" in path:
            contents = parser.compile(scss_file=path)
        else:
            f = open(path)
            contents = f.read()
            f.close()

        output.append(contents)

    return Response("\n".join(output), mimetype="text/css")


@app.route("/assets/images/<path:filename>")
def send_static_img(filename):
    directory = os.path.join(os.getcwd(), "assets", "images")
    return send_from_directory(directory, filename)


@app.route("/views/<widget_name>.html")
def widget_html(widget_name):
    html = "%s.html" % widget_name
    path = os.path.join(os.getcwd(), "widgets", widget_name, html)
    if os.path.isfile(path):
        f = open(path)
        contents = f.read()
        f.close()
        return contents


@app.route("/events")
def events():
    if xyzzy.using_events:
        event_stream_port = request.environ["REMOTE_PORT"]
        current_event_queue = Queue.Queue()
        xyzzy.events_queue[event_stream_port] = current_event_queue
        current_app.logger.info(
            "New Client %s connected. Total Clients: %s" %
            (event_stream_port, len(xyzzy.events_queue))
        )

        # Start newly connected client off by pushing the current last events
        for event in xyzzy.last_events.values():
            current_event_queue.put(event)
        return Response(
            pop_queue(current_event_queue),
            mimetype="text/event-stream",
        )

    return Response(xyzzy.last_events.values(), mimetype="text/event-stream")


def pop_queue(current_event_queue):
    while True:
        data = current_event_queue.get()
        yield data


def close_stream(*args, **kwargs):
    event_stream_port = args[2][1]
    del xyzzy.events_queue[event_stream_port]
    print(
        "Client %s disconnected. Total Clients: %s" %
        (event_stream_port, len(xyzzy.events_queue))
    )
