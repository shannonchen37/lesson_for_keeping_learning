# -*- coding: utf-8 -*-

import urllib, urllib2, sys
import ssl
import cv2
import base64
import json


def gender(img_name, upper_wear, upper_color, num):
    max_re = 0
    max_re_index = 0
    max_left = max_right = max_top = max_bottom = 0
    emotion = None
    max_rectangle_geder = "none"
    context = ssl._create_unverified_context()
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=xxxxxxx&client_secret=xxxxxxx'
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request, context=context)
    content1 = response.read()
    img = cv2.imread(img_name)
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    f = open(img_name, 'rb')
    image = base64.b64encode(f.read())
    image64 = str(image).encode("utf-8")
    params = {"image":''+image64+'',"image_type":"BASE64","face_field":"expression,gender,faceshape,age,race,emotion", "max_face_num":10}
    params = urllib.urlencode(params).encode("utf-8")
    access_token = content1.split("\"")[13]
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request, context=context)
    content = response.read()
    dict_info = json.loads(content)
    print "================================="
    print content
    print "================================="
    male_num = 0
    female_num = 0
    try:
        face_list = dict_info["result"]["face_list"]
    except:
        return "none", 0, 0
    for i in range(len(face_list)):
        left = int(face_list[i]["location"]["left"])
        top = int(face_list[i]["location"]["top"])
        right = int(face_list[i]["location"]["left"] + face_list[i]["location"]["width"])
        bottom = int(face_list[i]["location"]["top"] + face_list[i]["location"]["height"])
        if face_list[i]["gender"]["type"] == "male":
            male_num += 1
        else:
            female_num += 1
        print "aaaaaaaa", (right-left) * (bottom-top)
        if (right-left) * (bottom-top) > max_re:
            max_re = (right-left) * (bottom-top)
            max_re_index = i
            max_left = left
            max_right = right
            max_top = top
            max_bottom = bottom
    cv2.putText(img, face_list[max_re_index]["gender"]["type"], (max_left-10, max_bottom+40), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
    cv2.rectangle(img, (max_left, max_top), (max_right, max_bottom), (0, 0, 255), 2)
    cv2.putText(img, "Age:" + str(face_list[max_re_index]["age"]), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(img, "Skin color:" + str(face_list[max_re_index]["race"]["type"]), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(img, "Wearing:" + str(upper_color) + ' ' + str(upper_wear), (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.imwrite("./person_result"+str(num)+".jpg", img)
    return face_list[max_re_index]["gender"]["type"], face_list[max_re_index]["age"], face_list[max_re_index]["race"]["type"]


def judge_expression(n):
    e = None
    if n == "None":
        e = 0
    elif n == "smile":
        e = 1
    elif n == "laugh":
        e = 2
    return e


if __name__ == '__main__':
    gender("./gender_result11.jpg", "none", "none", 1)
