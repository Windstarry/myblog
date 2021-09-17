#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   models.py
@Time    :   2021/09/16 11:23:50
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    def __repr__(self):
	    return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #user_id字段已作为一个外键初始化了，这表明它引用了users表中的id值
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post {}'.format(self.body)
