#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   email.py
@Time    :   2021/09/24 16:10:07
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from flask_mail import Message
from app import mail
from flask import render_template
from app import app
from threading import Thread

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[myblog] 重置密码',
               sender=app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

                                    
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()