#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-11-09

from db import MyDataBase

db = MyDataBase.get_db()

class GrowRecord(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	event = db.Column(db.String(80))
	date = db.Column(db.DateTime)
	extra_text = db.Column(db.Text)

	def __init__(self, event, date, extra_text):
		self.event = event
		self.date = date
		self.extra_text = extra_text

	def __repr__(self):
		return "Event {0.event}, DateTime {0.date}, extra_text {0.extra_text}".format(self)



class Diary(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime)
	text = db.Column(db.Text)
	tags = db.Column(db.String(80))

	def __init__(self, date, text, tags):
		self.date = date
		self.text = text
		self.tags = tags

	def __repr__(self):
		return "{0.date} {0.tags}".format(self)

class Picture(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime)
	name = db.Column(db.String(256))
	path = db.Column(db.String(1024))
	thumbnail = db.Column(db.String(1024))

	def __init__(self, date, name, path, thumbnail):
		self.date = date
		self.name = name
		self.path = path
		self.thumbnail = thumbnail

	def __repr__(self):
		return "{0.name} {0.path}".format(self)