#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-11-09

# import application
from forms import RecordForm
from flask import Flask, render_template, request
from db import db
from db_model import GrowRecord

def index():
    if request.method == 'POST':
        return render_template('index.html')

    form = RecordForm()
    return render_template('index.html', form=form), 200


def submit():
    rc = GrowRecord(request.form['event'], request.form['date'], request.form['extra_text'])
    db.session.add(rc)
    db.session.commit()
    return render_template('submit.html', form=request.form), 200

def show():
    rc = GrowRecord.query.all()
    print(rc)
    return render_template('show.html', items=rc), 200

def register_all(register):
	register.add_route(submit, '/submit', methods=['POST'])
	register.add_route(index, '/', methods=['GET', 'POST'])
	register.add_route(show, '/show', methods=['GET'])



