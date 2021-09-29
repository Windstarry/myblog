#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2021/09/28 10:49:26
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import views