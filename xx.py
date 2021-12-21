# -*- coding: utf-8 -*-
# @Time    : 2021/12/21 9:43 上午
# @Author  : ddy
# @FileName: xx.py
# @github  : https://github.com/ddy-ddy


def search(info):
    '''
    info:"#南昌,@北京"
    #为标题
    @为地点
    ￥为时间:2021年12月11日
    '''
    title, place, time = "", "", ""
    try:
        info = info.split(",")
        for item in info:
            if item[0] == "#":
                title = item[1:]
            elif item[0] == '@':
                place = item[1:]
            elif item[0] == '￥':
                time = item[1:]
        if time:
            time = time.replace("年", "-")
            time = time.replace("月", "-")
            time = time.replace("日", "")
    except:
        pass
    return [title.strip(), place.strip(), time.strip()]


if __name__ == '__main__':
    print(search("#南昌,@北京,￥2021年12月21日"))
