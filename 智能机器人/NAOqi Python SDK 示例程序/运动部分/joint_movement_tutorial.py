#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
"""
代码名称：joint_movement_tutorial.py
代码功能：检验Pepper机器人移动关节功能
黑胡椒机器人技术有限公司开发
"""
import qi
from colorama import Fore, init
init(autoreset=True)


class joint:
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        # 声明本例中需要的参数
        self.count = 0
        self.get_service(qiApp)
        self.disable_auto_mode()
        self.set_parameter()
        self.joint_move()
        qiApp.stop()

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头
        print(Fore.GREEN + u"[I]: 取消自主模式中")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        # 取消了自主模式，机器人会低头，通过站立初始化让机器人抬起头
        self.RobotPosture.goToPosture("StandInit", 0.5)

    def set_parameter(self):
        # 设置机器人说话的语言和语速,设置机器人头部固定不随着移动变化
        self.Motion.setStiffnesses("Head",1.0)
        self.TextToSpeech.setLanguage("English")

    def get_service(self, qiApp):
        # 声明本例中需要的服务
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")
        self.RobotPosture = qiApp.session.service("ALRobotPosture")
        self.Motion = qiApp.session.service("ALMotion")
        self.TextToSpeech = qiApp.session.service("ALTextToSpeech")

    def joint_move(self):
        self.Motion.moveInit()
        self.TextToSpeech.say("I'm about to turn my head")
        self.Motion.setAngles("HeadYaw", 0.2, 1)

    def __del__(self):
        print(Fore.GREEN + u"[I]: 程序运行结束")

if __name__ == "__main__":
    joint_intance = joint()

