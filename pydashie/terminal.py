import SocketServer
import compago
import os
import server
import shutil
import sys


app = compago.Application()


@app.command
def new(name):
  """Sets up ALL THE THINGS needed for your dashboard project."""
  shutil.copytree(
      os.path.dirname(os.path.abspath(__file__)) + "/skeleton", name
  )


@app.command
def start(name):
    SocketServer.BaseServer.handle_error = server.close_stream
    sys.path.append('.')
    exec("import %s as app" % name)
    app.run(server.app, server.xyzzy)
