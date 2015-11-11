#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-11-09

from flask.ext.sqlalchemy import SQLAlchemy

db = None

def init_db(app):
	global db 
	db = SQLAlchemy(app)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/xxs?charset=utf8'
	db.init_app(app)
	db.create_all()
