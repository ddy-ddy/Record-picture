# -*- coding: utf-8 -*-
# @Time    : 2021/12/17 10:52 上午
# @Author  : ddy
# @FileName: show_page_view.py
# @github  : https://github.com/ddy-ddy
'''
展示页面的视图:
包含以下内容:
1.index
2.登陆
3.登出
'''
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from record_picture import app, db
from record_picture.models import User, login_password


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        info = login_password.query.first()

        if email == info.email and password == info.password:
            print("登陆成功")
            return render_template("show_page/index.html")
        else:
            print("登陆失败")
            return render_template("show_page/index.html")
    return render_template("show_page/index.html")
