#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
""""
代码名称：people_track.py
代码功能：利用ALTracker的API接口实现Pepper机器人追踪人体的功能
黑胡椒机器人技术有限公司开发
"""
import qi
from colorama import Fore, init
init(autoreset=True)
import thread
import time


class pepper_follow:
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        # self.follow_enable为Track功能的开关
        self.follow_enable = False
        # 注册Track目标时使用
        self.people_id = -1
        self.get_service(qiApp)
        self.disable_auto_mode()
        self.start_people_detection()
        self.set_parameter()
        self.start_track()

    def get_service(self, qiApp):
        # 获取本次案例中需要的服务
        self.Tracker = qiApp.session.service("ALTracker")
        self.RobotPosture = qiApp.session.service("ALRobotPosture")
        self.PeoplePerception = qiApp.session.service("ALPeoplePerception")
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")
        self.TextToSpeech = qiApp.session.service("ALTextToSpeech")
        self.Memory = qiApp.session.service("ALMemory")
        self.Motion = qiApp.session.service("ALMotion")

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头，取消自主模式后重新站好
        print(Fore.GREEN + u"[I]: 取消自主模式中")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        self.RobotPosture.goToPosture("StandInit", 0.5)

    def start_people_detection(self):
        # Pepper追踪人之前需要先注册目标，因此我们需要先进行人体检测，获取到目标人体的id来进行目标的注册
        self.PeoplePerception.subscribe("People")
        self.People_Detection = self.Memory.subscriber("PeoplePerception/PeopleDetected")
        self.People_Detection.signal.connect(self.callback_people_dete)

    def set_parameter(self):
        # 设置成true时，所有其他可选的检测（比如脸、运动等）都将停用
        self.PeoplePerception.setFastModeEnabled(True)
        self.Tracker.setRelativePosition([1, 0, 0, 0.1, 0.1, 0])
        # 设置追踪模式
        mode = "Move"
        self.Tracker.setMode(mode)

    def start_track(self):
        # 开始追踪功能
        self.follow_enable = True
        arg = tuple([1])
        thread.start_new_thread(self.follow, arg)
        # 进行30s
        time.sleep(30)
        # 停止追踪功能
        self.follow_enable = False

    def callback_people_dete(self, msg):
        print (Fore.GREEN + u"[I]: 检测到人")
        self.people_id = msg[1][0][0]

    def follow(self, arg):
        # 开始Track功能之前，检测是否已经检测到人
        while self.follow_enable:
            if self.people_id == -1:
                print(Fore.YELLOW + u"[W]: 没有检测到人，无法开始Track功能。请前后调整一下。")
                time.sleep(1)
                continue
            else:
                self.Motion.moveInit()
                self.Tracker.registerTarget("People", self.people_id)
                print(Fore.GREEN + u"[I]: 目标注册成功，开始Track功能")
                break
        # 开始Track功能
        self.Tracker.track("People")
        while self.follow_enable:
            # 获得机器人躯干坐标系下距离目标的距离
            target_position = self.Tracker.getTargetPosition(0)
            if not target_position:
                continue
            # 距离大于2m，进行语音提醒
            if target_position[0] > 2:
                self.TextToSpeech.say("please slow down, I can not follow you.")
        self.Tracker.stopTracker()
        self.Tracker.unregisterAllTargets()

    def __del__(self):
        print (Fore.GREEN + u"[I]: 退出程序中……")
        self.Tracker.stopTracker()
        self.Tracker.unregisterAllTargets()
        self.PeoplePerception.unsubscribe("People")


if __name__ == "__main__":
    follow_model = pepper_follow()
