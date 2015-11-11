#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-11-09

# wtforms and flask.ext.wtf both has a form class, 
# so it will be overwrite if in wrong sequence.
from wtforms import *
from flask.ext.wtf import Form
from wtforms.validators import *

class RecordForm(Form):
    """docstring for RecordForm"""
    event = StringField('事件', validators=[Required()])
    date = StringField('时间', validators=[Required()])
    extra_text = StringField('备注')
    submit = SubmitField('提交')
