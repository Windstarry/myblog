#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   errors.py
@Time    :   2021/09/16 11:23:40
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from flask import render_template
from app import app,db

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500