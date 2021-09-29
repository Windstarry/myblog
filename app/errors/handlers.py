#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   handlers.py
@Time    :   2021/09/27 16:43:11
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from flask import render_template
from app.ext import db
from app.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
	return render_template('errors/404.html'), 404

@bp.app_errorhandler(505)
def internal_error(error):
	db.session.rollback()
	return render_template('errors/500.html'), 500