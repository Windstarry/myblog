#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   views.py
@Time    :   2021/09/16 11:23:55
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from os import abort
from app import app,db
from flask import render_template, flash, redirect, url_for
from flask import request
from flask import g
from app.forms import LoginForm,RegistrationForm,EditProfileForm,PostForm,EditPostForm
from flask_login import current_user, login_user,logout_user,login_required
from werkzeug.urls import url_parse
from flask_babel import _
from flask_babel import get_locale
from app.models import User, Post
from datetime import datetime
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.forms import ResetPasswordForm



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('你的记录已发表'))
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='主页',form=form, posts=posts.items,next_url=next_url, prev_url=prev_url)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,next_url=next_url, prev_url=prev_url)


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
    return render_template('register.html', title='注册', form=form)


@app.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            #发送密码重置电子邮件
            send_password_reset_email(user)
        flash('登录邮箱查看链接重置密码')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='重置密码', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('密码已重置')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)
    # posts = user.followed_posts().all()
    # return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('你的修改已提交')
        return redirect(url_for('user',username = current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='编辑个人信息', form=form)


@app.route('/follow/<username>')
def follow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user is None:
        flash(_('用户 %(username)s 未找到', username=username))
        return redirect(url_for('index'))
    if current_user.is_following(user):
        flash(_('用户 %(username)s 已关注', username=username))
        return redirect(url_for('user',username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('关注用户 %(username)s', username=username))
    return redirect(url_for('user',username=username))


@app.route('/unfollow/<username>')
def unfollow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user is None:
        flash("未找到该用户")
        return redirect(url_for('index'))
    if current_user.is_following(user):
        current_user.unfollow(user)
        db.session.commit()
        flash("取消关注{}".format(username))
        return redirect(url_for('user',username=username))


@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html',posts = [post])


@app.route('/edit_post/<int:id>', methods = ['GET','POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user.id != post.user_id :
        abort(403)
    form = EditPostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('文章已更新')
        return redirect(url_for('post',id = post.id))
    elif request.method == 'GET':
        form.body.data = post.body
        return render_template('edit_post.html', form=form)



@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    #g.locale = str(get_locale())
    g.locale = 'zh_CN' if str(get_locale()).startswith('zh') else str(get_locale())

    
