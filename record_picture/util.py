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
import exifread
import requests

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


def get_info_from_image(path_name):
    with open(path_name, 'rb') as f:
        exif_dict = exifread.process_file(f)
        try:
            # 经度
            lon_ref = exif_dict["GPS GPSLongitudeRef"].printable
            lon = exif_dict["GPS GPSLongitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            lon = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / float(lon[3]) / 3600
            if lon_ref != "E":
                lon = lon * (-1)
            # 纬度
            lat_ref = exif_dict["GPS GPSLatitudeRef"].printable
            lat = exif_dict["GPS GPSLatitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            lat = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / float(lat[3]) / 3600
            if lat_ref != "N":
                lat = lat * (-1)
            x_y_info = list((lon, lat))  # 经纬度(维度,精度)
        except:
            x_y_info = None
        try:
            date = str(exif_dict['EXIF DateTimeOriginal']).split(" ")[0].replace(":", "-")  # 拍摄时间
        except:
            date = None
        try:
            device = exif_dict['Image Model']  # 拍摄设备
        except:
            device = None

    return x_y_info, date, device


# 高德地图地址解析获取经纬度
def gaodde(address):
    try:
        key = "ae7201c9d81da4c1a221f2f2452fd7aa"
        parameters = {'key': key, 'address': address}
        base = 'https://restapi.amap.com/v3/geocode/geo'
        response = requests.get(base, parameters)
        answer = response.json()["geocodes"][0]["location"]
        return answer.split(",")
    except:
        return None
