#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   forms.py
@Time    :   2021/09/16 11:23:45
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from flask_wtf import FlaskForm#
#导入这些类
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
	username = StringField('用户名', validators=[DataRequired()])
	password = PasswordField('密码', validators=[DataRequired()])
	remember_me = BooleanField('记住我')
	submit = SubmitField('登录')