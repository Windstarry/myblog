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
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    def __repr__(self):
	    return '<User {}>'.format(self.username)