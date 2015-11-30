#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-11-09
from flask.ext.sqlalchemy import SQLAlchemy

class MyDataBase(object):
    """docstring for MyDataBase"""

    app = None
    db = None
    
    @classmethod
    def get_db(cls):
        if not cls.app:
            print("MyDataBase app is None")
            return None
        if cls.db:
            return cls.db
        cls.init_db()
        return cls.db

    @classmethod
    def init_db(cls):
        if not cls.app:
            print("MyDataBase app is None")
            return

        cls.db = SQLAlchemy(cls.app)

        #cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@192.168.10.101/xxs?charset=utf8'

        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/xxs.db'

        # cls.db.init_app(cls.app)
        from db_model import GrowRecord
        cls.db.create_all()



        
