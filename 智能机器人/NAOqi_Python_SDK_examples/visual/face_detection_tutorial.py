#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
"""
代码名称：face_detection_tutorial.py
代码功能：检验Pepper机器人人脸检测功能
黑胡椒机器人技术有限公司开发
"""
import qi
import time
from colorama import init, Fore
init(autoreset=True)


class face_detect:
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        # switch变量确保程序一次只能进行一次回调函数，防止程序超线程
        self.switch = True
        self.if_detected_face = False
        self.get_service(qiApp)
        self.set_parameter()
        self.disable_auto_mode()
        self.face_detection()
        self.__del__()
        qiApp.stop()

    def get_service(self, qiApp):
        # 获取本次案例中需要的服务
        self.TextToSpeech = qiApp.session.service("ALTextToSpeech")
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")
        self.FaceDetection = qiApp.session.service("ALFaceDetection")
        self.Memory = qiApp.session.service("ALMemory")
        self.RobotPosture = qiApp.session.service("ALRobotPosture")

    def face_detection(self):
        # 开启检测人脸的引擎
        self.FaceDetection.subscribe("MyFaceDetectedDemo")
        if not self.FaceDetection.isRecognitionEnabled():
            self.FaceDetection.setRecognitionEnabled()
        self.face_detection_sub = self.Memory.subscriber("FaceDetected")
        self.face_detection_sub.signal.connect(self.callback_face_detection)
        print(Fore.GREEN + u"[I]: 开始检测人脸!")
        self.TextToSpeech.say("Please look at me and wait for a moment")
        while not self.if_detected_face:
            time.sleep(1)
        self.FaceDetection.unsubscribe("MyFaceDetectedDemo")

    def callback_face_detection(self, msg):
        # 检测到人脸机器人会发声并在屏幕上显示已检测到的信息
        if self.switch == False:
            return
        self.switch = False
        print(Fore.GREEN + u"[I]: 检测到人脸！")
        self.TextToSpeech.say("face detected!")
        self.if_detected_face = True

    def set_parameter(self):
        # 设置机器人说话的语言和语速
        self.TextToSpeech.setParameter("speed", 75.0)
        self.TextToSpeech.setLanguage("English")

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头
        print(Fore.GREEN + u"[I]: 取消自主模式中")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        # 取消了自主模式，机器人会低头，通过站立初始化让机器人抬起头
        self.RobotPosture.goToPosture("StandInit", 0.5)

    def __del__(self):
        print(Fore.GREEN + u"[I]: 程序运行结束")

if __name__ == "__main__":
    face_intance = face_detect()
