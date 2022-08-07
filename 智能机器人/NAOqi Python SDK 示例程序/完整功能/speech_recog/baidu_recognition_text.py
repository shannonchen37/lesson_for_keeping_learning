#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import wave
from pyaudio import PyAudio,paInt16
import json
import base64
import os
import requests
import time


RATE = "16000"
FORMAT = "wav"
CUID="wate_play"
DEV_PID = 1737

framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2


def get_token():
    server = "https://openapi.baidu.com/oauth/2.0/token?"
    grant_type = "client_credentials"
    #API Key
    client_id = "xxxxxxx"
    #Secret Key
    client_secret = "xxxxxxx"

    #拼url
    url ="%sgrant_type=%s&client_id=%s&client_secret=%s"%(server,grant_type,client_id,client_secret)
    #获取token
    res = requests.post(url)
    token = json.loads(res.text)["access_token"]
    # print token
    return token

def get_word(token, path):
    with open(path, "rb") as f:
        speech = base64.b64encode(f.read()).decode('utf8')
    size = os.path.getsize(path)
    headers = { 'Content-Type' : 'application/json'}
    url = "https://vop.baidu.com/server_api"
    data={
            "format":FORMAT,
            "rate":RATE,
            "dev_pid":DEV_PID,
            "speech":speech,
            "cuid":CUID,
            "len":size,
            "channel":1,
            "token":token,
        }

    req = requests.post(url,json.dumps(data),headers)
    try:
        result = json.loads(req.text)
    except Exception as e:
        print e
        return "none"
    return result["result"][0]


def main(path):
    try:
        token=get_token()
    except:
        return "00"
    try:
        ret = get_word(token, path)
        result = str(ret)
    except:
        print('失败了')
        return "00"
    print result
    return result
if __name__ == '__main__':
    main("./audio_record/recog.wav")
