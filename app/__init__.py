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
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(config['development'])
#数据库对象
db = SQLAlchemy(app)
#迁移引擎对象
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
#导入一个新模块models，它将定义数据库的结构
from app import views,models