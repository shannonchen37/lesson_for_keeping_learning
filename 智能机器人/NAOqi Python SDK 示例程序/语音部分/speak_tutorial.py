#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
"""
代码名称：speak_tutorial.py
代码功能：检验Pepper机器人说话功能
黑胡椒机器人技术有限公司开发
"""
import qi
import time
from colorama import Fore, init
init(autoreset=True)


class speak:
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        self.get_service(qiApp)
        self.set_parameter()
        self.disable_auto_mode()
        self.speak()
        self.__del__()
        qiApp.stop()

    def get_service(self, qiApp):
        # 声明需要的服务
        self.TextToSpeech = qiApp.session.service("ALTextToSpeech")
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")
        self.RobotPosture = qiApp.session.service("ALRobotPosture")
        self.AnimatedSpeech = qiApp.session.service("ALAnimatedSpeech")

    def set_parameter(self):
        # 将机器人的语音设置为英文，设置机器人语音的速度
        self.TextToSpeech.setParameter("speed", 75.0)
        self.TextToSpeech.setLanguage("English")

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头
        print(Fore.GREEN + u"[I]: 取消自主模式中……")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        # 取消了自主模式，机器人会低头，通过站立初始化让机器人抬起头
        self.RobotPosture.goToPosture("StandInit", 0.5)

    def speak(self):
        print(Fore.GREEN + u"[I]: 开始说话部分")
        # 说话功能的主体
        self.TextToSpeech.setLanguage("English")
        self.TextToSpeech.say("Hi, my name is pepper, nice to meet you")
        time.sleep(1)
        self.AnimatedSpeech.say("Start Animated Speech")
        time.sleep(1)
        self.AnimatedSpeech.say("I'm changing my language into Chinese")
        time.sleep(1)
        self.TextToSpeech.setLanguage("Chinese")
        self.AnimatedSpeech.say("你好，我是 Pepper，很高兴认识你")
        time.sleep(1)

    def __del__(self):
        print(Fore.GREEN + u"[I]: 程序运行结束")

if __name__ == "__main__":
    speak_intance = speak()
