import os
from Queue import Queue
from glob import glob

from coffeescript import compile_file as compile_coffeescript_file
from flask import Response
from flask import current_app
from flask import render_template
from flask import request
from flask import send_from_directory
from scss import Scss

from pydashie import app
from pydashie import xyzzy
from pydashie import PYDASHIE_APP_NAME


@app.route("/")
def main():
    return render_template("main.html", title="pyDashie")


@app.route("/assets/application.js")
def javascripts():
    if not hasattr(current_app, "javascripts"):
        javascripts = _get_javascripts()

        output = []
        for path in javascripts:
            output.append("// JS: %s\n" % path)
            if ".coffee" in path:
                print("Compiling Coffee for %s " % path)
                contents = \
                    compile_coffeescript_file(path).encode("ascii", "ignore")
            else:
                print("Reading JS for %s " % path)
                f = open(path)
                contents = f.read()
                f.close()

            output.append(contents)

        current_app.javascripts = "\n".join(output)

    return Response(current_app.javascripts, mimetype="application/javascript")


def _get_javascripts():
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

    javascripts = []
    for js in ordered_script_names:
        script_filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "javascripts",
            js
        )
        javascripts.append(script_filename)
    for ext in ["js", "coffee"]:
        javascripts.extend(
            glob(
                os.path.join(
                    os.getcwd(),
                    PYDASHIE_APP_NAME,
                    "assets/**/*.%s"
                ) % ext
            )
        )
    for ext in ["js", "coffee"]:
        javascripts.extend(
            glob(
                os.path.join(
                    os.getcwd(),
                    PYDASHIE_APP_NAME,
                    "widgets/**/*.%s"
                ) % ext
            )
        )
    return javascripts


@app.route("/assets/application.css")
def application_css():
    parser = Scss()

    stylesheets = _get_stylesheets()

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


def _get_stylesheets():
    stylesheets = []
    for ext in ["css", "scss"]:
        stylesheets.extend(
            glob(
                os.path.join(
                    os.getcwd(),
                    PYDASHIE_APP_NAME,
                    "assets/**/*.%s"
                ) % ext
            )
        )
    for ext in ["css", "scss"]:
        stylesheets.extend(
            glob(
                os.path.join(
                    os.getcwd(),
                    PYDASHIE_APP_NAME,
                    "widgets/**/*.%s"
                ) % ext
            )
        )
    return stylesheets


@app.route("/assets/images/<path:filename>")
def send_static_img(filename):
    directory = os.path.join(os.getcwd(), PYDASHIE_APP_NAME, "assets", "images")
    return send_from_directory(directory, filename)


@app.route("/views/<widget_name>.html")
def widget_html(widget_name):
    html = "%s.html" % widget_name
    path = os.path.join(
        os.getcwd(),
        PYDASHIE_APP_NAME,
        "widgets",
        widget_name,
        html
    )
    if os.path.isfile(path):
        f = open(path)
        contents = f.read()
        f.close()
        return contents


@app.route("/events")
def events():
    if xyzzy.using_events:
        event_stream_port = request.environ["REMOTE_PORT"]
        current_event_queue = Queue()
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
