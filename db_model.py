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



