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
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('用户名', validators=[DataRequired()])
	password = PasswordField('密码', validators=[DataRequired()])
	remember_me = BooleanField('记住我')
	submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    #Email是WTForms附带的stock validator，它将确保用户在此字段中键入的内容与电子邮件地址的结构相匹配（省了正则去匹配这是否为一个邮箱地址）
    email = StringField('电子邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '重新输入密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名已注册，请更换用户名')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('电子邮箱已注册，请更换邮箱')


class EditProfileForm(FlaskForm):
	username = StringField('用户名', validators=[DataRequired()])
	about_me = TextAreaField('我的简介', validators=[Length(min=0, max=140)])
	submit = SubmitField('提交')

    #验证用户名
	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')