#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-11-09

# import application
from forms import RecordForm, DiaryForm, UploadForm
from flask import Flask, render_template, request, url_for, redirect, Blueprint, current_app, flash
from db import MyDataBase
from db_model import GrowRecord, Diary, Picture
from datetime import datetime, date, timedelta
from sqlalchemy import func
from werkzeug import secure_filename
import json
import os

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
    rc = GrowRecord.query.order_by(GrowRecord.date.desc()).paginate(
            page, 
            per_page=current_app.config['FLASK_COUNT_PER_PAGE'], 
            error_out=False)

    db = MyDataBase.get_db()
    try:
        day_sum = db.session.query(GrowRecord.event, func.count(GrowRecord.event)).\
            filter( GrowRecord.date >= date.today(), 
                    GrowRecord.date <= (date.today() + timedelta(days = 1))).\
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
    return redirect(url_for('main.index'))

def show():
    page = request.args.get('page', 1, type=int)
    event = request.args.get('event', None, type=str)
    # query_date = request.args.get('date', None, type=str)
    page = page if page > 0 else 1

    rc = None
    if event is not None:
        rc = GrowRecord.query.filter(
                GrowRecord.event==event, 
                GrowRecord.date >= date.today(), 
                GrowRecord.date <= (date.today() + timedelta(days = 1))).order_by(
                                            GrowRecord.date.desc()).paginate(page, 
                                            per_page=current_app.config['FLASK_COUNT_PER_PAGE'], 
                                            error_out=False)
    else:
        rc = GrowRecord.query.order_by(GrowRecord.date.desc()).paginate(
                page, 
                per_page=current_app.config['FLASK_COUNT_PER_PAGE'], 
                error_out=False)
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
    page = page if page > 0 else 1

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
    
    if kind == "pic":
        db = MyDataBase.get_db()
        rc = Picture.query.filter_by(id=id).first()
        full_path = rc.path
        print(full_path)
        if rc:
            try:
                db.session.delete(rc)
                db.session.commit()
                full_path = os.getcwd() + "/" + rc.path
                if os.path.exists(full_path):
                    os.remove(full_path)
                return "", 200
            except Exception as e:
                db.session.roll_back()    
    return "", 404

def draw():

    db = MyDataBase.get_db()
    result = { "name": "flare", "children": [] }
    try:
        for day in range(-10,1):
            
            day_sum = db.session.query(GrowRecord.event, func.count(GrowRecord.event)).\
                filter( GrowRecord.date >= (date.today()+ timedelta(days = day)), 
                        GrowRecord.date <= (date.today() + timedelta(days = day+1))).\
                group_by(GrowRecord.event).all()
            
            result["children"].append({ "name": day, 
                        "children" : [{ "name" :((date.today()+ timedelta(days = day))).strftime("%m-%d") + '\n' + itr[0], 
                        "size": itr[1] } for itr in day_sum ]})
        # print(result)
    except Exception:
        db.session.roll_back()
        return "", 404

    return json.dumps(result)

def upload(type):
    form = UploadForm()
    print(os.getcwd())
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        suffix = filename.split('.')[-1]
        if suffix not in ['jpg','png','bmp']:
            flash("不是图片哦")
        date_as_filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.'+suffix
        form.photo.data.save('static/pic/' + date_as_filename)
        rc = Picture(datetime.now(), date_as_filename, "static/pic/"+date_as_filename) 

        db = MyDataBase.get_db()
        # print(db)
        try:
            db.session.add(rc)
            db.session.commit()
        except Exception as e:
            full_path = os.getcwd() + "static/pic/" + date_as_filename
            if os.path.exists(full_path):
                os.remove(full_path)
            db.session.roll_back()
            return "", 404


    else:
        filename = None
    # return render_template('upload.html', form=form, filename=filename)
    return redirect(url_for('main.photos')), 200

def photos():
    form = UploadForm()
    page = request.args.get('page', 1, type=int)
    rc = Picture.query.order_by(Picture.date.desc()).paginate(
            page, 
            per_page=15, 
            error_out=False)
    items = rc.items
    return render_template("photo.html", form=form, paginate=rc, items=items), 200

def register_all(register):
    register.add_route(index, '/', methods=['GET'])
    register.add_route(submit, '/submit', methods=['POST'])
    register.add_route(diary, '/diary', methods=['GET', 'POST'])
    register.add_route(show, '/show', methods=['GET'])
    register.add_route(about, '/about', methods=['GET'])
    register.add_route(delete, '/delete/<kind>/<id>', methods=['GET'])
    register.add_route(draw, '/draw', methods=['GET'])
    register.add_route(upload, '/<type>/upload', methods=['POST'])
    register.add_route(photos, '/photo', methods=['GET'])

register_all(RouteRegister(main))

