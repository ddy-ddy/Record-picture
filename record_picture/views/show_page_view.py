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
from flask import render_template, request, url_for, redirect, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from record_picture import app, db
from record_picture.models import User


@app.route('/')
def index():
    return render_template("show_page_index.html")


# 登陆
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_name, password = request.form.get("username"), request.form.get("password")

        user = db.session.query(User).filter(User.login_name == login_name).first()

        if user:
            if check_password_hash(user.password_hash, password):
                flash("登陆成功")  # 登陆成功
                login_user(user)
                return redirect(url_for("index"))
            else:
                flash("1")  ##密码错误
                return redirect(url_for("login"))
        else:
            flash("2")  ##没有该账号,请注册！
            return redirect(url_for('register'))

    return render_template("login.html")


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        register_name, register_password = request.form.get("register_name"), request.form.get("register_password")
        user = db.session.query(User).filter(User.login_name == register_name).first()

        if user:
            flash("3")  # 该账号已注册,请登陆
            return redirect(url_for("login"))
        else:
            flash("注册成功")  # 注册成功
            new_user = User(login_name=register_name)
            new_user.set_password(register_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("index"))

    return render_template("register.html")


# 登出
def logout():
    pass
