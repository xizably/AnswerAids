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
from PIL import Image
from urllib import request
from urllib.parse import quote


"""
APP ID AK SK
"""
APP_ID = '10786178'
API_KEY = 'GUNE66AAYuy7XbfLfT62INfP'
SECRET_KEY = 'i4avkihy6jOSmebSQf814Fbs3oGHUBVc'


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


# 读取图片
def get_image_txt(image_path):
    with open(image_path, 'rb') as fp:
        img = fp.read()
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

        # 通用文字识别 500次/天免费
        # 如果有可选参数
        options = {"language_type": "CHN_ENG", "detect_direction": "false", "detect_language": "false",
                   "probability": "true"}
        # 带参数调用通用文字识别, 图片参数为本地图片
        get_result = client.basicGeneral(img, options)

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

        return get_result


# 问题关键要素提取
def get_key(txt_ques):
    txt_ques = str(txt_ques).replace('?', '').replace('不是', '') \
        .replace('什么', '').replace('以下', '') \
        .replace('下列', '').replace('不', '') \
        .replace('哪', '').replace('个', '') \
        .replace('正确的', '').replace('是', '')\
        .replace('属于', '').replace('说法', '')\
        .replace('哪一项', '').replace('说法', '')
    return txt_ques


# 用浏览器搜索关键字
def use_web_search(txt_ques):
    search_url = f'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=' \
                 + quote(txt_ques)
    webbrowser.open(search_url)


# 问题搜索
def ques_search(txt_ques):
    search_url = f'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=' \
                 + quote(txt_ques)
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      r'Chrome/64.0.3282.119 Safari/537.36',
        'Referer': search_url
    }
    req = request.Request(search_url, headers=headers)
    page = request.urlopen(req).read().decode('utf-8')
    return page


# 结果汇总
def sum_result(page_data, key_value, result_count):
    if len(key_value) < 0:
        return '未识别问题···'
    # sr = key_value[0]
    if len(key_value) == 1:
        return '未识别问题···'
    for i in range(1, len(key_value)):
        result_count[i - 1] = page_data.count(key_value[i])
        # sr += f'\n{key_value[i]}: {result_count[i - 1]}'
    # if result_count == [0, 0, 0]:
    #     return sr
    # if page_data.count('不') > 0 or page_data.count('错误') > 0:
    #     sug_index = result_count.index(min(result_count))
    # else:
    #     sug_index = result_count.index(max(result_count))
    # sr += f'\n\n建议答案：{key_value[sug_index + 1]}'
    # return sr
    return result_count
