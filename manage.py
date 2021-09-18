#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   manage.py
@Time    :   2021/09/16 11:23:29
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from app import app, db
from flask_script import Manager
from app.models import User, Post

manager = Manager(app)

'''
app.shell_context_processor装饰器注册了一个作为shell 上下文功能的函数,
当运行flask shell命令时，它将调用此函数并在shell会话中注册它返回的项,
函数返回字典而不是列表的原因是：
对于每个项目，我们还须提供一个名称，在这个名称下，它将在shell中被引用，由字典的键给出。
'''

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


if __name__ == '__main__':
    #开发者模式
    app.run(debug=True)
    #非开发者模式
    # manager.run()   