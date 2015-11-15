#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-11-09

__author__ = 'Matthew Gao'


# from db_model import *
from flask import Flask, render_template, request, current_app
from flask_bootstrap import Bootstrap
from db import MyDataBase

bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'development key'
    app_ctx = app.app_context()
    app_ctx.push()
    current_app.config['FLASK_COUNT_PER_PAGE'] = 8
    bootstrap.init_app(app)
    MyDataBase.app = app
    MyDataBase.init_db()
    from route import main as main_blue_print
    app.register_blueprint(main_blue_print)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
