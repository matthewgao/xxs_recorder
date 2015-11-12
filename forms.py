#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-11-09

# wtforms and flask.ext.wtf both has a form class, 
# so it will be overwrite if in wrong sequence.
from wtforms import *
from flask.ext.wtf import Form
from wtforms.validators import *
from datetime import datetime

class RecordForm(Form):
    """docstring for RecordForm"""
    event = SelectField('事件', validators=[Required()], 
        choices=[('吃饭','吃饭'), ('睡觉','睡觉'), ('便便', '便便'), 
                ('尿尿', '尿尿'), ('洗澡', '洗澡'), ('哭闹', '哭闹'), ('醒来', '醒来')])
    date = StringField('时间', default=str(datetime.now()))
    extra_text = StringField('备注', default='无')
    # submit = SubmitField('提交')
