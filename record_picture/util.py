# -*- coding: utf-8 -*-
# @Time    : 2021/12/18 9:47 上午
# @Author  : ddy
# @FileName: util.py
# @github  : https://github.com/ddy-ddy

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from wtforms import SubmitField
from record_picture import app
from PIL import Image

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


class Upload_image_Form(FlaskForm):
    photo = FileField(validators=[
        FileAllowed(photos, u'只能上传图片！'),
        FileRequired('...')])
    submit = SubmitField(u'上传照片')


def change_image_size(path_name):
    # 打开该图片
    image = Image.open(path_name)

    # 设定尺寸
    image = image.resize(size=(1024, 1024), resample=Image.BILINEAR)

    # 保存
    image.save(path_name)
