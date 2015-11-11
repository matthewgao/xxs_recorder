#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-11-09

__author__ = 'Matthew Gao'


# from db_model import *
from flask import Flask, render_template, request
from db import db, init_db
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.debug = True
app.secret_key = 'development key'

class RouteRegister(object):
    """docstring for RouteRegister"""
    def __init__(self, app):
        super(RouteRegister, self).__init__()
        self.app = app

    def add_route(self, res, url, **kargs):
        res = self.app.route(url, **kargs)(res)

init_db(app)
Bootstrap(app)

from route import register_all
register_all(RouteRegister(app))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)