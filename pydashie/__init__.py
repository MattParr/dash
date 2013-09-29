import os
from flask import Flask
from event_handler import EventHandler


xyzzy = EventHandler()

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "templates"))


import pydashie.server
