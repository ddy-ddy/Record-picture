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
            if check_password_hash(user.password_hash, password):  # 验证密钥
                flash("登陆成功")  # 登陆成功
                login_user(user)  # 建立会话
                return redirect(url_for("user_index"))
            else:
                flash("1")  # 密码错误
                return redirect(url_for("login"))
        else:
            flash("2")  # 没有该账号,请注册！
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
            print("注册成功")
            new_user = User(login_name=register_name)
            new_user.set_password(register_password)
            db.session.add(new_user)
            db.session.commit()
            flash("flag_welcome")
            login_user(new_user)  # 建立会话
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
    country = request.form.get("country")
    iphone = request.form.get("iphone")
    # 修改数据库的信息
    if name != None and name:
        user_info.profile_name = name
    if country != None and country:
        user_info.country = country
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
        name, place, device_name = request.form.get("name"), request.form.get("place"), request.form.get("device")
        # 更新图像
        if form.validate_on_submit():
            filename = photos.save(form.photo.data, name=f"{user_info.login_name}/user_images/{name}.")  # 保存图片
        else:
            flash("图片未上传成功")
            return redirect(url_for("upload"))  # 重新上传照片
        file_url = str(photos.url(filename))
        print(file_url)
        # 获取图像的地址信息和时间信息
        image_x_y, time, device = get_info_from_image(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
        device = str(device_name) + str(device)
        if time == None:
            time = "2020-12-10"  # 设置默认时间
        if image_x_y == None:
            # 根据城市名得到x,y
            image_x_y = gaodde(place)

        # 将图像信息添加到数据库中
        pic = Picture(login_name=user_info.login_name, picture_url=file_url,
                      title=name, device=str(device), place=place, time=str(time), place_x_y=str(image_x_y))
        db.session.add(pic)
        db.session.commit()
        flash("上传成功")

    return render_template("user_upload.html", user_info=user_info, form=form)


# 删除照片
@app.route('/delete/<int:P_id>', methods=["POST"])
@login_required
def delete_picture(P_id):
    info = db.session.query(Picture).filter(Picture.id == P_id).first()
    try:
        path = f"{os.getcwd()}/user_uploads/{info.login_name}/user_images/" + str(
            info.picture_url.split("/")[-1])
        os.remove(path)  # 删除文件
    except:
        pass
    db.session.delete(info)
    db.session.commit()
    return redirect(url_for("show_all_pictures"))


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
        search_info = request.form.get("search_info").split(",")  ##得到的内容为'#南昌,@北京'

        pictures_info = db.session.query(Picture).filter(Picture.title == search_info[0]).all()
        return render_template("user_pictures.html", user_info=user_info, pictures_info=pictures_info,
                               tag=search_info[0])
    return render_template("user_search.html", user_info=user_info)


# 地图
@app.route("/map", methods=["GET", "POST"])
@login_required
def map():
    user_info = current_user
    url_info = db.session.query(Picture).filter(
        Picture.login_name == user_info.login_name and Picture.picture_url != None).all()
    place_info = []
    for item in url_info:
        temp_info = [eval(item.place_x_y), str(item.picture_url)]
        place_info.append(temp_info)
    return render_template("user_map.html", user_info=user_info, place_info=place_info)
