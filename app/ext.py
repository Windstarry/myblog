#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   ext.py
@Time    :   2021/09/29 11:26:30
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_babel import Babel, lazy_gettext as _l

bootstrap = Bootstrap()
db = SQLAlchemy()
login = LoginManager()
csrf = CSRFProtect()
mail = Mail()
moment = Moment()
migrate = Migrate()
babel = Babel()

login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')