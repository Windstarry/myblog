#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   views.py
@Time    :   2021/09/16 11:23:55
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    #用户
    user = {'username':'Windstarry'}
    #创建一个列表：帖子。里面元素是两个字典，每个字典里元素还是字典，分别作者、帖子内容。
    posts = [
        {
        'author': {'username':'John'},
        'body':'Beautiful day in Portland!'
        },
        {
        'author': {'username':'Susan'},
        'body':'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {},remember_me={}'.format(form.username.data,form.remember_me.data))
		return redirect(url_for('index'))
	return render_template('login.html', title='登录', form=form)