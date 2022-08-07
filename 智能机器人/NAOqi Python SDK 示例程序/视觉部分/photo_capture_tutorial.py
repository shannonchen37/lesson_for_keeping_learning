#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
"""
代码名称：photo_capture_tutorial.py
代码功能：检验Pepper机器人拍照与平板展示功能
黑胡椒机器人技术有限公司开发
"""
import qi
from colorama import init, Fore
init(autoreset=True)


class photo_cap:
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        self.get_service(qiApp)
        self.disable_auto_mode()
        self.set_parameter()
        self.takepic()
        self.show_image()
        qiApp.stop()

    def get_service(self, qiApp):
        # 获取本次案例中需要的服务
        self.TextToSpeech = qiApp.session.service("ALTextToSpeech")
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")
        self.Memory = qiApp.session.service("ALMemory")
        self.PhotoCapture = qiApp.session.service("ALPhotoCapture")
        self.RobotPosture = qiApp.session.service("ALRobotPosture")
        self.TabletService = qiApp.session.service("ALTabletService")

    def set_parameter(self):
        # 将机器人的语音设置为英文，设置机器人语音的速度
        self.TextToSpeech.setParameter("speed", 75.0)
        self.TextToSpeech.setLanguage("English")

    def takepic(self):
        # 拍照功能的主体
        self.TextToSpeech.say("I'm going to take a picture")
        self.PhotoCapture.takePictures(1, '/home/nao/.local/share/PackageManager/apps/boot-config/html',
                                       'image_example')
        self.TextToSpeech.say("picture's taken")
        print(Fore.GREEN + u"[I]: 照片拍摄成功")

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头
        print(Fore.GREEN + u"[I]: 取消自主模式中")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        self.RobotPosture.goToPosture("StandInit", 0.5)

    def show_image(self):
        # 将主机电脑的照片送至Pepper机器人，通过平板展示出来
        self.TabletService.hideImage()
        self.TabletService.showImageNoCache("http://198.18.0.1/apps/boot-config/image_example.jpg")

    def __del__(self):
        print(Fore.GREEN + u"[I]: 程序运行结束")

if __name__ == "__main__":
    photo_instance = photo_cap()