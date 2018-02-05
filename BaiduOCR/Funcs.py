# -*- coding: utf-8 -*-
"""
用到的工具：
ADB（PC连接安卓工具 - 路径加到path下）
Tesseract OCR（光学字符识别工具 - 路径加到path下）
Pillow（Python库 - 图片裁剪工具）
"""
import os
import webbrowser
import ssl
import sys

from aip.ocr import AipOcr
from PIL import Image
from urllib import request
from urllib.parse import quote


# OCR APP ID AK SK
OCR_APP_ID = '10786178'
OCR_API_KEY = 'GUNE66AAYuy7XbfLfT62INfP'
OCR_SECRET_KEY = 'i4avkihy6jOSmebSQf814Fbs3oGHUBVc'
# Natural language analysis API - AppID APIKey SecretKey
NLA_APP_ID = '10794818'
NLA_API_KEY = 'dwTYQ1gqY6Im35yZBP9NCKQj'
NLA_SECRET_KEY = 'DFl3XcFSObyaCGHAwixPukn2uSCkTNp2'


# 获取手机屏幕截图
def get_img(img_name):
    os.system('@echo off')
    os.system(f'del {img_name}')
    os.system(f'adb shell /system/bin/screencap -p /sdcard/{img_name}')
    os.system(f'adb pull /sdcard/{img_name} {img_name}')


# 图片裁剪加工
def crop_img(img_name, save_name):
    img = Image.open(img_name)
    # img_new = img.convert('1')
    # img_new = img.convert('L')
    img_new = img.convert('P')
    img_new_rgb = img_new.convert('RGB')
    x = 40
    y = 175
    w = 460
    h = 445
    region = img_new_rgb.crop((x, y, x + w, y + h))
    region.save(save_name, 'jpeg')
    img.close()


# 识别图片中的文字
def get_image_arry(image_path):
    with open(image_path, 'rb') as fp:
        img = fp.read()
        client = AipOcr(OCR_APP_ID, OCR_API_KEY, OCR_SECRET_KEY)

        # 通用文字识别 500次/天免费
        # 如果有可选参数
        options = {"language_type": "CHN_ENG", "detect_direction": "false", "detect_language": "false",
                   "probability": "true"}
        # 带参数调用通用文字识别, 图片参数为本地图片
        get_txt = client.basicGeneral(img, options)

        # 调用通用文字识别, 图片参数为本地图片
        # get_result = client.basicGeneral(img)

        # url = ''
        # client.basicGeneral(url)
        # options = {"language_type": "CHN_ENG", "detect_direction": "true", "detect_language": "true", "probability": "true"}
        # get_result = client.basicGeneral(img, options)

        # 调用通用文字识别（高精度版） 50次/天免费
        # get_result = client.basicAccurate(img);

        # options = {"detect_direction": "true", "probability": "true"}
        # get_result = client.basicAccurate(img, options)

        get_result = get_txt.get('words_result')
        result_len = len(get_result)
        result_arry = [''] * result_len
        for i in range(0, result_len):
            result_arry[i] = get_result[i].get('words')
        while len(result_arry) > 4:
            result_arry[0] += result_arry[1]
            result_arry.remove(result_arry[1])
        result_arry[0] = result_arry[0][result_arry[0].index('.') + 1:]
        return result_arry


# 获取百度API的access_token
def get_access_token():
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
           f'client_id={NLA_API_KEY}&client_secret={NLA_SECRET_KEY}'
    req = request.Request(host)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    req.add_header('User-Agent', r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 r'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36')
    access_token = request.urlopen(req).read()
    return access_token


# 问题关键要素提取
def get_key(access_token, ques_txt):
    url = f'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?access_token={access_token}&'


# 用浏览器搜索关键字
def use_web_search(ques_txt):
    search_url = f'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=' \
                 + quote(ques_txt)
    webbrowser.open(search_url)


# 问题搜索并返回统计结果
def ques_search(ques_txt):
    search_url = f'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=' \
                 + quote(ques_txt[0])
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      r'Chrome/64.0.3282.119 Safari/537.36',
        'Referer': search_url
    }
    req = request.Request(search_url, headers=headers)
    page_data = request.urlopen(req).read().decode('utf-8')
    # if len(ques_txt) < 4:
    #     return '未识别问题···'
    sr = ques_txt[0]
    for i in range(1, len(ques_txt)):
        sr += f'\n{ques_txt[i]}: {page_data.count(ques_txt[i])}'
    return sr



