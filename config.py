# -*- coding: utf-8 -*-
# @Time    : 2021/12/17 10:43 上午
# @Author  : ddy
# @FileName: config.py
# @github  : https://github.com/ddy-ddy


import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "abc"  # 设置表单交互密钥

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    basedir = os.path.abspath(os.path.dirname(__file__))
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'user_uploads')  # 用户文件上传的位置


# 开发环境配置信息
class DevConfig(Config):
    ENV = 'development'
    DEBUG = True


# 线上环境配置信息
class PrdConfig(Config):
    ENV = 'production'
    DEBUG = False


# 测试环境配置信息
class TestingConfig(Config):
    ENV = 'test'
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False


# 访问结构
config = {
    'dev': DevConfig,
    'prd': PrdConfig,
    'testing': TestingConfig,
    'default': DevConfig,
}
