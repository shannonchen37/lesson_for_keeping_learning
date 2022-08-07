#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
"""
代码名称：memory_tutorial.py
代码功能：学习机器人消息机制
黑胡椒机器人技术有限公司开发
"""
import qi
import time
from colorama import Fore, init
init(autoreset=True)


class memory:
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        self.count = 0
        self.get_service(qiApp)
        self.disable_auto_mode()
        self.data_process()
        self.__del__()
        qiApp.stop()

    def get_service(self, qiApp):
        # 获取本次案例中需要的服务
        self.Memory = qiApp.session.service("ALMemory")
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")
        self.RobotPosture = qiApp.session.service("ALRobotPosture")

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头，取消自主模式后重新站好
        print(Fore.GREEN + u"[I]: 取消自主模式中")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        self.RobotPosture.goToPosture("StandInit", 0.5)

    def data_process(self):
        # 利用getData函数可以直接获得消息的内容
        isHeadTouched = self.Memory.getData("Device/SubDeviceList/Head/Touch/Middle/Sensor/Value")
        print(Fore.GREEN + u"[I]: 通过getData获得的数据是： " + str(isHeadTouched))
        # 若绑定回调函数，只有在消息触发时会激活回调函数，并把消息一并传送至回调函数中
        HeadTouched_sub = self.Memory.subscriber("MiddleTactilTouched")
        HeadTouched_sub.signal.connect(self.callback_headtouch)
        time.sleep(30)
        
    def callback_headtouch(self, msg):
        if msg != 0.0:
            print(Fore.GREEN + u"[I]: 通过回调函数获取的数据是： " + str(msg))

    def __del__(self):
        print(Fore.GREEN + u"[I]: 程序运行结束")

if __name__ == "__main__":
    memory_intance = memory()