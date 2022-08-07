#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
代码名称：audio_recog_Web_API_tutorial.py
代码功能：利用百度Web API进行语音识别
根据百度AI官方样例代码改编
"""
import json
import base64
import os
import requests


RATE = "16000"
FORMAT = "wav"
CUID = "wate_play"
DEV_PID = 1737
framerate = 16000
audio_path = "./audio/test.wav"
NUM_SAMPLES = 2000
channels = 1
sampwidth = 2
TIME = 2
# 换成自己的API Key
client_id = "xxxxx"
# 换成自己的Secret Key
client_secret = "xxxxx"


# 获取access_token
def get_token():
    server = "https://openapi.baidu.com/oauth/2.0/token?"
    grant_type = "client_credentials"
    # 拼接url
    url="%sgrant_type=%s&client_id=%s&client_secret=%s"%(server, grant_type, client_id, client_secret)
    # 获取token
    res = requests.post(url)
    token = json.loads(res.text)["access_token"]
    return token


# 上传至云端进行语音识别
def get_word(token, path):
    with open(path, "rb") as f:
        speech = base64.b64encode(f.read()).decode('utf8')
    size = os.path.getsize(path)
    headers = { 'Content-Type' : 'application/json'}
    url = "https://vop.baidu.com/server_api"
    # data输入了一部分所需要的参数
    data = {
            "format": FORMAT,
            "rate": RATE,
            "dev_pid": DEV_PID,
            "speech": speech,
            "cuid": CUID,
            "len": size,
            "channel": 1,
            "token": token,
        }
    req = requests.post(url, json.dumps(data), headers)
    try:
        result = json.loads(req.text)
    except Exception as e:
        print e
        return "none"
    return result["result"][0]


def main(path):
    token = get_token()
    try:
        ret = get_word(token, path)
        result = str(ret)
        print result
    except Exception as e:
        print e


if __name__ == '__main__':
    main(audio_path)
