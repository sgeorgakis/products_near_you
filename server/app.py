# -*- coding: utf-8 -*-

import os
import logging

from flask import Flask

from server.api import api
import server.db
from server.json_encoder import CustomJSONEncoder


def create_app(settings_overrides=None):
    logging.basicConfig(
            format='%(asctime)s %(levelname)s %(name)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            level=logging.DEBUG)
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    app.products = server.db.load_data(get_data_path())
    configure_settings(app, settings_overrides)
    configure_blueprints(app)
    return app


def configure_settings(app, settings_override):
    data_path = get_data_path()

    app.config.update({
        'DEBUG': True,
        'TESTING': False,
        'DATA_PATH': data_path
    })
    if settings_override:
        app.config.update(settings_override)


def configure_blueprints(app):
    app.register_blueprint(api)


def get_data_path():
    parent = os.path.dirname(__file__)
    return os.path.join(parent, '..', 'data')
