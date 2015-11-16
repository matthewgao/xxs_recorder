#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-11-09

# import application
from forms import RecordForm, DiaryForm
from flask import Flask, render_template, request, url_for, redirect, Blueprint, current_app, flash
from db import MyDataBase
from db_model import GrowRecord, Diary
from datetime import datetime, date, timedelta
from sqlalchemy import func

main = Blueprint('main', __name__)
# current_app.config['FLASK_COUNT_PER_PAGE'] = 8

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
    # rc = GrowRecord.query.order_by(GrowRecord.date).all()
    rc = GrowRecord.query.order_by(GrowRecord.date.desc()).paginate(page, 
        per_page=current_app.config['FLASK_COUNT_PER_PAGE'], error_out=False)

    db = MyDataBase.get_db()
    try:
        day_sum = db.session.query(GrowRecord.event, func.count(GrowRecord.event)).\
            filter(GrowRecord.date >= date.today(), GrowRecord.date <= (date.today() + timedelta(days = 1))).\
            group_by(GrowRecord.event).all()
    except Exception:
        db.session.roll_back()
        return "", 404
    # print(day_sum)

    items = rc.items
    return render_template('index.html', form=form, items=items, paginate=rc, sum=day_sum), 200

def submit():
    rc = GrowRecord(request.form['event'], 
            datetime.strptime(request.form['date'], '%Y-%m-%d %H:%M:%S'), 
            request.form['extra_text'])
    db = MyDataBase.get_db()
    # print(db)
    try:
        db.session.add(rc)
        db.session.commit()
    except Exception as e:
        db.session.roll_back()
        return "", 404
    # return render_template('submit.html', form=request.form), 200
    return redirect(url_for('main.show'))

def show():
    page = request.args.get('page', 1, type=int)
    # rc = GrowRecord.query.order_by(GrowRecord.date).all()
    rc = GrowRecord.query.order_by(GrowRecord.date.desc()).paginate(page, 
        per_page=current_app.config['FLASK_COUNT_PER_PAGE'], error_out=False)
    # print(rc)
    items = rc.items

    return render_template('show.html', items=items, paginate=rc), 200

def about():
    return render_template('about.html'), 200

def diary():
    if request.method == 'POST':
        if not request.form['text']:
            flash("请写点什么先")
            return redirect(url_for('main.diary'))

        rc = Diary(datetime.now(), request.form['text'], request.form['tags'])
        db = MyDataBase.get_db()
        try:
            db.session.add(rc)
            db.session.commit()
        except Exception as e:
            db.session.roll_back()
            return "", 404
        
        return redirect(url_for('main.diary'))
    form = DiaryForm()
    page = request.args.get('page', 1, type=int)
    # rc = Diary.query.order_by(Diary.date).all()
    try:
        rc = Diary.query.order_by(Diary.date.desc()).paginate(page, 
            per_page=current_app.config['FLASK_COUNT_PER_PAGE'], error_out=False)
    except Exception as e:
        db.session.roll_back()
        return "", 404
    items = rc.items
    return render_template('diary.html', form=form, items=items, paginate=rc), 200

def delete(kind, id):
    if kind == "grow_record":
        db = MyDataBase.get_db()
        rc = GrowRecord.query.filter_by(id=id).first()
        if rc:
            try:
                db.session.delete(rc)
                db.session.commit()
                return "", 200
            except Exception as e:
                db.session.roll_back()
             
    return "", 404


def register_all(register):
    register.add_route(index, '/', methods=['GET'])
    register.add_route(submit, '/submit', methods=['POST'])
    register.add_route(diary, '/diary', methods=['GET', 'POST'])
    register.add_route(show, '/show', methods=['GET'])
    register.add_route(about, '/about', methods=['GET'])
    register.add_route(delete, '/delete/<kind>/<id>', methods=['GET'])

register_all(RouteRegister(main))

