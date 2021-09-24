#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Time    :   2021/09/16 11:23:20
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
import os


class BaseConfig(object):
    """项目配置核心类"""
    #调试模式
    DEBUG=True
    # 配置日志
    # LOG_LEVEL = "DEBUG"
    LOG_LEVEL = "INFO"
    # #数据库连接格式
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@localhost:3306/test?charset=utf8"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = False
    # 数据库连接池的大小
    SQLALCHEMY_POOL_SIZE=10
    #指定数据库连接池的超时时间
    SQLALCHEMY_POOL_TIMEOUT=10
    #确定每页显示多少个项目数
    POSTS_PER_PAGE = 20
    #增加邮箱基本信息
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')#客户端授权密码

class DevelopmentConfig(BaseConfig):
    #数据库连接格式
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'test'
    USENAME = 'root'
    PASSWORD = '123456'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{usename}:{password}@{host}:{port}/{database}?charset=utf8".format( usename = USENAME,
                                                                                                                    password = PASSWORD,
                                                                                                                    host = HOST,
                                                                                                                    port = PORT,
                                                                                                                    database = DATABASE,)


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
   #数据库连接格式
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'myblog'
    USENAME = 'root'
    PASSWORD = '123456'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{usename}:{password}@{host}:{port}/{database}?charset=utf8".format( usename = USENAME,
                                                                                                                    password = PASSWORD,
                                                                                                                    host = HOST,
                                                                                                                    port = PORT,
                                                                                                                    database = DATABASE,)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}