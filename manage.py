#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   manage.py
@Time    :   2021/09/16 11:23:29
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from app import app
from flask_script import Manager

manager = Manager(app)


if __name__ == '__main__':
    #开发者模式
    app.run(debug=False)
    #非开发者模式
    # manager.run()   