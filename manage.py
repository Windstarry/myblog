#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   manage.py
@Time    :   2021/09/16 11:23:29
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from app import create_app, db, cli
from app.models import User,Post

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
	return {'db':db, 'User':User, 'Post':Post}

if __name__ == '__main__':
    app.run()