#!/usr/bin/env python
# -*- coding=UTF-8 -*-
#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: app.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-03-14 21:04:34
#*************************************************************************
from flask import Flask
from config import load_config


def register_routes(app):
    from .views import site
    app.register_blueprint(site)


def register_form(app):
    from flask_wtf.csrf import CsrfProtect
    csrf = CsrfProtect()
    csrf.init_app(app)



def register(app):
    register_routes(app)
    register_form(app)


def create_app():
    app = Flask(__name__, static_folder='static')
    config = load_config()
    app.config.from_object(config)
    return app

app = create_app()
register(app)

@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413

@app.errorhandler(404)
def request_entity(error):
    return 'File Too Large', 404
