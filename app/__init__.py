#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2021/09/16 11:33:50
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy  # 从包中导入类
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import config  
from flask import current_app
from app.auth import bp as auth_bp
from app.errors import bp as errors_bp
from app.main import bp as main_bp
from app.ext import bootstrap, db, login,mail, moment,migrate,babel


# db = SQLAlchemy()
# migrate = Migrate()
# login = LoginManager()  # 初始化Flask-Login
# login.login_view = 'auth.login'
# login.login_message = _l('Please log in to access this page.')
# mail = Mail()
# bootstrap = Bootstrap()
# moment = Moment()
# babel = Babel()



def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config['development'])
    register_extensions(app)
    register_blueprints(app)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/myblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('myblog startup')
    return app



def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)
    

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


#导入一个新模块models，它将定义数据库的结构
# remove errors from this import!
#from app import views,models


