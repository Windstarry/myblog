#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   email.py
@Time    :   2021/09/24 16:10:07
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from threading import Thread
from flask import current_app
from flask_mail import Message
from app.ext import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,args=(current_app._get_current_object(), msg)).start()