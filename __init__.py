#!/usr/bin/env python3
import os
from flask import Flask

"""
app = Flask(__name__)  # that means that your app name will be the same as the file

app.config.from_object(__name__)  # load config from this file, app.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASK_SETTINGS', silent=True)
"""
