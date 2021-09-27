#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2021/09/16 11:33:50
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from flask import Flask
from flask import request
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel,lazy_gettext as _l


app = Flask(__name__)
app.config.from_object(config['development'])



#数据库对象
db = SQLAlchemy(app)
#迁移引擎对象
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l("请登录访问")

mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

#导入一个新模块models，它将定义数据库的结构
from app import views,models,errors

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/myblog.log', maxBytes=10240,backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Myblog startup')
