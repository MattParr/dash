import SocketServer
import compago
import os
import server
import shutil
import sys

from pydashie import PYDASHIE_APP_NAME as app_name


app = compago.Application()


@app.command
def new():
    """Sets up ALL THE THINGS needed for your dashboard project."""
    shutil.copytree(
        os.path.dirname(os.path.abspath(__file__)) + "/skeleton", app_name
    )


@app.command
def start():
    SocketServer.BaseServer.handle_error = server.close_stream
    sys.path.append('.')
    exec("import %s as app" % app_name)
    app.run(server.app, server.xyzzy)
