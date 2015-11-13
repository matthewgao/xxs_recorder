#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-11-09

# import application
from forms import RecordForm
from flask import Flask, render_template, request, url_for, redirect, Blueprint, current_app
from db import MyDataBase
from db_model import GrowRecord
from datetime import datetime

main = Blueprint('main', __name__)
current_app.config['FLASK_COUNT_PER_PAGE'] = 8

class RouteRegister(object):
    """docstring for RouteRegister"""
    def __init__(self, app):
        super(RouteRegister, self).__init__()
        self.app = app

    def add_route(self, res, url, **kargs):
        res = self.app.route(url, **kargs)(res)

def index():
    # if request.method == 'POST':
    #     return render_template('index.html')
    page = request.args.get('page', 1, type=int)
    print(page)
    form = RecordForm()
    rc = GrowRecord.query.order_by(GrowRecord.date).all()
    rc = GrowRecord.query.order_by(GrowRecord.date).paginate(page, 
        per_page=current_app.config['FLASK_COUNT_PER_PAGE'], error_out=False)

    items = rc.items
    return render_template('index.html', form=form, items=items, paginate=rc), 200

def submit():
    rc = GrowRecord(request.form['event'], request.form['date'], request.form['extra_text'])
    db = MyDataBase.get_db()
    db.session.add(rc)
    db.session.commit()
    # return render_template('submit.html', form=request.form), 200
    return redirect(url_for('main.show'))

def show():
    page = request.args.get('page', 1, type=int)
    rc = GrowRecord.query.order_by(GrowRecord.date).all()
    rc = GrowRecord.query.order_by(GrowRecord.date).paginate(page, 
        per_page=current_app.config['FLASK_COUNT_PER_PAGE'], error_out=False)
    # print(rc)
    items = rc.items
    return render_template('show.html', items=items, paginate=rc), 200

def about():
    return render_template('about.html'), 200

def register_all(register):
    register.add_route(submit, '/submit', methods=['POST'])
    register.add_route(index, '/', methods=['GET'])
    register.add_route(show, '/show', methods=['GET'])
    register.add_route(about, '/about', methods=['GET'])

register_all(RouteRegister(main))

