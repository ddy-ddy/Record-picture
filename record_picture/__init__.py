# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)

# 加载配置文件
app.config.from_object(config["testing"])

# 初始各种扩展库
db = SQLAlchemy(app)  # 初始化数据库
login_manager = LoginManager(app)  # 实例化login扩展类


@login_manager.user_loader
def load_user(user_id):  # user_loader回调函数,从数据库中加载用户
    from record_picture.models import User
    user = User.query.get(int(user_id))  # 创建用户加载回调函数,接受用户ID作为参数
    return user  # 返回用户对象


@app.context_processor  # 模板上下处理函数
def inject_user():  # 函数名可以随意修改
    from record_picture.models import User
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}


login_manager.login_view = 'login'

from record_picture.views import show_page_view
from record_picture import commands
