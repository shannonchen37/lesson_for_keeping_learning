#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
"""
代码名称：move_to_tutorial.py
代码功能：检验Pepper机器人简单移动功能
黑胡椒机器人技术有限公司开发
"""
import qi
import time
from colorama import Fore, init
init(autoreset=True)


class move:
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        self.get_service(qiApp)
        self.set_parameter()
        self.disable_auto_mode()
        self.move()
        qiApp.stop()

    def get_service(self, qiApp):
        # 获取本次案例中需要的服务
        self.Motion = qiApp.session.service("ALMotion")
        self.TextToSpeech = qiApp.session.service("ALTextToSpeech")
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")

    def set_parameter(self):
        # 设置机器人说话的语言和语速,设置机器人头部固定不随着移动变化
        self.Motion.setStiffnesses("Head",1.0)
        self.TextToSpeech.setLanguage("English")

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头
        print(Fore.GREEN + u"[I]: 取消自主模式中")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")

    def move(self):
        # 机器人移动功能的主体
        self.TextToSpeech.say("I'm about to move forward")
        time.sleep(3)
        self.Motion.moveInit()
        self.Motion.moveTo(1, 0, 0, _async=True)
        time.sleep(3)
        self.TextToSpeech.say("I'm about to turn around")
        self.Motion.moveTo(0, 0, -3.14, _async=True)
        time.sleep(5)

    def __del__(self):
        print(Fore.GREEN + u"[I]: 程序运行结束")

if __name__ == "__main__":
    move_intance = move()
