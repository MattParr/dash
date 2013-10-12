import os
from flask import Flask
from event_handler import EventHandler

PYDASHIE_APP_NAME = 'pydashie_app'

xyzzy = EventHandler()

app = Flask(
    __name__,
    template_folder=os.path.join(os.getcwd(), PYDASHIE_APP_NAME, "templates"),
)

import pydashie.server
