# -*- coding: utf-8 -*-
"""
用到的工具：
ADB（PC连接安卓工具 - 路径加到path下）
Tesseract OCR（光学字符识别工具 - 路径加到path下）
Pillow（Python库 - 图片裁剪工具）
"""
import os
import webbrowser

from aip.ocr import AipOcr
from aip import AipNlp
from PIL import Image
from urllib import parse
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
    img_size_x, img_size_y = img.size
    x = int(2 / 27 * img_size_x)
    y = int(35 / 192 * img_size_y)
    w = int(23 / 27 * img_size_x)
    h = int(89 / 192 * img_size_y)
    region = img_new_rgb.crop((x, y, x + w, y + h))
    region.save(save_name, 'jpeg')
    img.close()


# 视觉技术 - 识别图片中的文字
def get_image_arry(image_path):
    with open(image_path, 'rb') as fp:
        img = fp.read()
        client = AipOcr(OCR_APP_ID, OCR_API_KEY, OCR_SECRET_KEY)

        # 通用文字识别 500次/天免费
        # 如果有可选参数
        # 带参数调用通用文字识别, 图片参数为本地图片
        # options = {"language_type": "CHN_ENG", "detect_direction": "false", "detect_language": "false",
        #            "probability": "true"}
        # get_txt = client.basicGeneral(img, options)

        # 调用通用文字识别, 图片参数为本地图片
        # get_txt = client.basicGeneral(img)

        # 调用通用文字识别, 图片参数为网络图片
        # url = ''
        # client.basicGeneral(url)
        # options = {"language_type": "CHN_ENG",
        #            "detect_direction": "true",
        #            "detect_language": "true",
        #            "probability": "true"}
        # get_txt = client.basicGeneral(img, options)

        # 调用通用文字识别（高精度版） 50次/天免费
        # get_txt = client.basicAccurate(img);
        options = {"detect_direction": "true", "probability": "true"}
        get_txt = client.basicAccurate(img, options)

        get_result = get_txt.get('words_result')
        result_len = len(get_result)
        result_arry = [''] * result_len
        for i in range(0, result_len):
            result_arry[i] = get_result[i].get('words')
        while len(result_arry) > 4:
            # print(result_arry)
            result_arry[0] += result_arry[1]
            result_arry.remove(result_arry[1])
        if result_arry[0].count('.') > 0:
            point_index = result_arry[0].index('.')
            if point_index == 1 or point_index == 2:
                result_arry[0] = result_arry[0][result_arry[0].index('.') + 1:]
        else:
            result_arry[0] = result_arry[0][1:]
        return result_arry


# 词法分析 - 问题关键要素提取
def speech_analysis(ques_txt):
    client = AipNlp(NLA_APP_ID, NLA_API_KEY, NLA_SECRET_KEY)
    key_txt = client.lexer(ques_txt)
    words = key_txt.get('items')
    keys_txt = []
    # print(words)
    for word in words:
        word_type = word.get('pos')
        if word_type not in ('w', 'u', 'r', 'v', 'p', 'd'):
            kst = word.get('item')
            keys_txt.append(kst)
        else:
            continue
    return keys_txt


# 用浏览器搜索关键字
def use_web_search(ques_txt):
    search_url = f'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=' \
                 + quote(ques_txt)
    webbrowser.open(search_url)


# 问题搜索并返回统计结果
def ques_search(ques_txt):
    # ses = {'baidu': f'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=',
    #        'google': f'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='}
    # search_url = ses.get(search_engine) + quote(ques_txt[0])
    search_url = f'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=' \
                 + quote(ques_txt[0])
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      r'Chrome/64.0.3282.119 Safari/537.36',
        'Referer': search_url
    }
    req = request.Request(search_url, headers=headers)
    page_data = request.urlopen(req).read().decode('utf-8')
    sr = ques_txt[0]
    for i in range(1, len(ques_txt)):
        sr += f'\n{ques_txt[i]}: {page_data.count(ques_txt[i])}'
    return sr


# 根据选项统计分析问题关键字

