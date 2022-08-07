#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
代码名称：people_feature_detection_Web_API_tutorial.py
代码功能：利用Baidu API进行人体特征检测，包括人的性别，年龄段，上身和下身衣服类型与颜色
根据百度AI官方样例代码改编，参考网址：https://ai.baidu.com/docs#/Body-API/ce1b59da
"""
import urllib, urllib2
import ssl
import cv2
import base64
import json
from colorama import Fore, init
init(autoreset=True)
# 应用的API Key
client_id = "xxxxxx"
# 应用的Secret Key
client_secret = "xxxxxxx"


def get_token():
    context = ssl._create_unverified_context()
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request, context=context)
    content1 = response.read()
    access_token = content1.split("\"")[13]
    return access_token


def feature(img_name):
    # 调取Baidu AI的人体检测功能，获取性别、年龄、以及衣服的种类和颜色
    context = ssl._create_unverified_context()
    img = cv2.imread(img_name)
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_attr"
    f = open(img_name, 'rb')
    image = base64.b64encode(f.read())
    image64 = str(image).encode("utf-8")
    # 设置参数，选择需要检测的内容
    params = {"image":''+image64+'',"image_type":"BASE64",
              "type":"gender,age,lower_wear,upper_wear,upper_color,lower_color"}
    params = urllib.urlencode(params).encode("utf-8")
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(request, context=context)
    content = response.read()
    dict_info = json.loads(content)
    try:
        people_list = dict_info["person_info"]
    except Exception as e:
        print (Fore.RED + u"[E]: 发生错误，程序退出")
        return
    for i in range(len(people_list)):
        # 获取检测到的人体的上下左右的位置
        left = int(people_list[i]["location"]["left"])
        top = int(people_list[i]["location"]["top"])
        right = int(people_list[i]["location"]["left"] + people_list[i]["location"]["width"])
        bottom = int(people_list[i]["location"]["top"] + people_list[i]["location"]["height"])
        # 利用OpenCV框出人体的位置
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
        # 获取检测到的性别、年龄、以及衣服的种类和颜色
        gender = people_list[i]["attributes"]["gender"]["name"].encode("UTF-8")
        age = people_list[i]["attributes"]["age"]["name"].encode("UTF-8")
        lower_color = people_list[i]["attributes"]["lower_color"]["name"].encode("UTF-8")
        upper_color = people_list[i]["attributes"]["upper_color"]["name"].encode("UTF-8")
        lower_wear = people_list[i]["attributes"]["lower_wear"]["name"].encode("UTF-8")
        upper_wear = people_list[i]["attributes"]["upper_wear"]["name"].encode("UTF-8")
        print (Fore.GREEN + (u"[I]: 检测到" + gender + age + u"穿着" + lower_color + u"色的" + lower_wear + u"和" + upper_color + u"色的" + upper_wear))
    cv2.imwrite("./pictures/image.jpg", img)


if __name__ == '__main__':
    feature("./pictures/image.jpg")
