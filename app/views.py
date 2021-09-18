#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   views.py
@Time    :   2021/09/16 11:23:55
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from app import app,db
from flask import render_template, flash, redirect, url_for
from flask import request
from app.forms import LoginForm,RegistrationForm
from flask_login import current_user, login_user,logout_user,login_required
from werkzeug.urls import url_parse
from app.models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
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
    return render_template('index.html', title='Home', posts=posts)



@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    current_user变量来自Flask-Login,可在处理过程中随时使用，以表示请求客户端的用户对象。
    此变量的值可以是数据库中的用户的对象Flask-Login通过上述提供的用户加载器回调读取的,
    如果用户尚未登录，则可以是特殊的匿名用户对象
    is_authenticated可以方便地检查用户是否登录,当用户已经登录时，只需重定向到/index页面
    '''
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
		#重定向到 next 页面
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='登录', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜您已经注册成功')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)