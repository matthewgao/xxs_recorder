#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-11-09

__author__ = 'Matthew Gao'

from flask import Flask, render_template, request
from flask.ext.wtf import Form
from wtforms import *
from wtforms.validators import *

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html')

    form = RecordForm()
    return render_template('index.html', form=form), 200

@app.route('/submit', methods=['POST'])
def submit():
    print(request.form)
    return 'submitted', 200

class RecordForm(Form):
    """docstring for RecordForm"""
    name = StringField('Event', validators=[Required()])
    submit = SubmitField('submit')
    #     self.submit = SubmitField('submit')
    # def __init__(self):
    #     super(RecordForm, self).__init__()
    #     self.name = StringField('Event', validators=[Required()])
    #     self.submit = SubmitField('submit')
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)