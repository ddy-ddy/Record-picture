# -*- coding: utf-8 -*-
# @Time    : 2021/12/17 10:52 上午
# @Author  : ddy
# @FileName: show_page_view.py
# @github  : https://github.com/ddy-ddy
'''
路由
'''
from flask import render_template, request, url_for, redirect, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from record_picture import app, db
from record_picture.models import User, Picture
from .util import *
import os


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
                return redirect(url_for("user_index"))
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
            flash("flag_welcome")
            return redirect(url_for("user_index"))

    return render_template("register.html")


# 登出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


# 个人信息页面
@app.route('/profile', methods=["GET", "POST"])
@login_required  # 视图保护
def user_index():
    # 从数据库提取信息
    user_info = current_user
    form = Upload_image_Form()
    return render_template("user_profile.html", user_info=user_info, form=form)


# 更改头像
@app.route('/change_profile_img', methods=["GET", "POST"])
@login_required
def change_form():
    user_info = current_user
    form = Upload_image_Form()
    # 更新图像
    if form.validate_on_submit():
        filename = photos.save(form.photo.data, name=f"{user_info.login_name}/user_profile/img.")  # 保存图片
        change_image_size(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))  # 修改图片大小
        file_url = photos.url(filename)
    else:
        file_url = None
    # 更新数据库
    if file_url:
        user_info.picture_link = file_url
    db.session.add(user_info)
    db.session.commit()
    return redirect(url_for("user_index"))


# 更改个人信息
@app.route('/change_profile_info', methods=["GET", "POST"])
@login_required
def change_info():
    user_info = current_user
    # 更新信息
    name = request.form.get("name")
    email = request.form.get("email")
    iphone = request.form.get("iphone")
    # 修改数据库的信息
    if name != None and name:
        user_info.profile_name = name
    if email != None and email:
        user_info.email = email
    if iphone != None and iphone:
        user_info.iphone = iphone
    db.session.add(user_info)
    db.session.commit()
    return redirect(url_for("user_index"))


# 上传照片
@app.route('/upload', methods=["GET", "POST"])
@login_required
def upload():
    user_info = current_user
    form = Upload_image_Form()

    if request.method == 'POST':
        # 获取图片信息
        name, place, device = request.form.get("name"), request.form.get("place"), request.form.get("device")
        # 更新图像
        if form.validate_on_submit():
            filename = photos.save(form.photo.data, name=f"{user_info.login_name}/user_images/{name}.")  # 保存图片
        else:
            filename = None
        file_url = photos.url(filename)
        # 将图像信息添加到数据库中
        pic = Picture(id=len(Picture.query.all()) + 1, login_name=user_info.login_name, picture_url=file_url,
                      title=name,
                      device=device, place=place)
        db.session.add(pic)
        db.session.commit()
        flash("上传成功")
    return render_template("user_upload.html", user_info=user_info, form=form)


# 展示照片
@app.route('/show_all_pictures', methods=["GET", "POST"])
@login_required
def show_all_pictures():
    user_info = current_user
    pictures_info = db.session.query(Picture).filter(Picture.login_name == user_info.login_name).all()
    return render_template("user_pictures.html", user_info=user_info, pictures_info=pictures_info, tag="所有照片")


# 搜索照片
@app.route('/search_pictures', methods=["GET", "POST"])
@login_required
def search_pictures():
    user_info = current_user
    if request.method == 'POST':
        search_info = request.form.get("search_info").split(",")  ##得到的内容为'南昌,北京'

        pictures_info = db.session.query(Picture).filter(Picture.title == search_info[0]).all()

        return render_template("user_pictures.html", user_info=user_info, pictures_info=pictures_info,
                               tag=search_info[0])

    return render_template("user_search.html", user_info=user_info)


# 地图
@app.route("/map", methods=["GET", "POST"])
@login_required
def map():
    user_info = current_user
    return render_template("user_map.html", user_info=user_info)
