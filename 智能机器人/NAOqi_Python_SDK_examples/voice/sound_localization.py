#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
"""
代码名称：sound_localization_tutorial.py
代码功能：检验Pepper机器人声源定位功能
黑胡椒机器人技术有限公司开发
"""
import qi
import time
from colorama import Fore, init
init(autoreset=True)


class sound_loc:
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        # 声明需要的变量，通过布尔型变量确保回调函数一次只运行一个
        self.switch = True
        self.get_service(qiApp)
        self.disable_auto_mode()
        self.Motion.moveInit()
        self.sound_localization()
        self.run()
        self.__del__()
        qiApp.stop()

    def sound_localization(self):
        # 声源定位功能的主体，激活声源定位的引擎并绑定回调函数
        self.TextToSpeech.say("Talk to me and I will turn to you")
        self.SoundLocalization.subscribe("SoundLocated")
        self.SoundLocalization.setParameter("Sensitivity", 0.7)
        self.sound_localization_sub = self.Memory.subscriber("ALSoundLocalization/SoundLocated")
        self.sound_localization_sub.signal.connect(self.callback_sound_localization)

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头
        print(Fore.GREEN + u"[I]: 取消自主模式中")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        self.RobotPosture.goToPosture("StandInit", 0.5)

    def callback_sound_localization(self, msg):
        if self.switch == False:
            return
        self.switch = False
        sound_loc = msg
        if sound_loc[1][2] > .5:
            print(Fore.BLUE + u"[I]: 移动中")
            self.Motion.moveTo(0, 0, sound_loc[1][0])
        self.switch = True

    def get_service(self, qiApp):
        # 声明需要的服务
        self.TextToSpeech = qiApp.session.service("ALTextToSpeech")
        self.RobotPosture = qiApp.session.service("ALRobotPosture")
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")
        self.Memory = qiApp.session.service("ALMemory")
        self.SoundLocalization = qiApp.session.service("ALSoundLocalization")
        self.Motion = qiApp.session.service("ALMotion")

    def run(self):
        # 程序结束后取消订阅话题
        time.sleep(20)
        self.SoundLocalization.unsubscribe("SoundLocated")

    def __del__(self):
          print(Fore.GREEN + u"[I]: 程序运行结束")

if __name__ == "__main__":
    sound_localize_intance = sound_loc()