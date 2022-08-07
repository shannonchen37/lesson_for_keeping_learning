#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
代码名称：people_detection_tutorial.py
代码功能：利用ALPeoplePerception的API接口实现Pepper机器人识别人体的功能
黑胡椒机器人技术有限公司开发
"""
import qi
from colorama import init, Fore
import time
init(autoreset=True)


class people_detection:
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        # self.if_in_callback变量确保程序一次只能进行一次回调函数，防止程序超线程
        self.if_in_callback = False
        self.get_service(qiApp)
        self.disable_auto_mode()
        self.set_parameter()
        self.start_people_detection()
        qiApp.stop()
        self.__del__()

    def get_service(self, qiApp):
        # 获取本次案例中需要的服务
        self.RobotPosture = qiApp.session.service("ALRobotPosture")
        self.PeoplePerception = qiApp.session.service("ALPeoplePerception")
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")
        self.TextToSpeech = qiApp.session.service("ALTextToSpeech")
        self.Memory = qiApp.session.service("ALMemory")

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头，取消自主模式后重新站好
        print(Fore.GREEN + u"[I]: 取消自主模式中")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        self.RobotPosture.goToPosture("StandInit", 0.5)

    def start_people_detection(self):
        # 开始人体检测
        print(Fore.GREEN + u"[I]: 开始检测人体，请站到Pepper前面")
        self.PeoplePerception.subscribe("MyPerceptionDemo")
        self.People_Dete = self.Memory.subscriber("PeoplePerception/PeopleDetected")
        self.People_Dete.signal.connect(self.callback_people_dete)
        final_time = time.time() + 20
        while time.time() < final_time:
            if self.if_in_callback == True:
                break
        self.PeoplePerception.unsubscribe("MyPerceptionDemo")

    def set_parameter(self):
        # 设置成true时，所有其他可选的检测（比如脸、运动等）都将停用
        self.PeoplePerception.setFastModeEnabled(True)
        self.TextToSpeech.setLanguage("English")

    def callback_people_dete(self, msg):
        if self.if_in_callback:
            return
        self.if_in_callback = True
        print (Fore.GREEN + u"[I]: 检测到人")
        self.TextToSpeech.say("people detected")
        time.sleep(2)

    def __del__(self):
        print(Fore.GREEN + u"[I]: 程序运行结束")


if __name__ == "__main__":
    people_detector = people_detection()
