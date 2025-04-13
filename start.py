from flaskwebgui import FlaskUI
from app import app
import os

FlaskUI(app=app, server="flask").run()
