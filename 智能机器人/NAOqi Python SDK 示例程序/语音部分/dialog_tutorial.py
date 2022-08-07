#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
"""
代码名称：dialog_tutorial.py
代码功能：检验Pepper机器人通过对话触发事件的逻辑功能
黑胡椒机器人技术有限公司开发
"""
import qi
import time
from colorama import Fore, init
init(autoreset=True)


class dialog:
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        self.switch = False
        # 机器人内部的.top文件路径
        self.topic_path = "/path/to/your/topic/file"
        self.get_service(qiApp)
        self.disable_auto_mode()
        self.set_parameter()
        self.start_dialog_engine()
        self.run()
        qiApp.stop()

    def start_dialog_engine(self):
        # 如果当前机器人中仍运行着其他的dialog文件，则先全部清空，再激活本代码中的.top文件
        if self.Dialog.getLoadedTopics('enu') != []:
            tmp = self.Dialog.getActivatedTopics()
            for item in tmp:
                self.Dialog.deactivateTopic(item)
        self.topic_name = self.Dialog.loadTopic(self.topic_path.encode('utf-8'))
        self.Dialog.activateTopic(self.topic_name)
        # 订阅对话的服务，激活对话功能
        self.Dialog.subscribe("Talking")
        print(Fore.GREEN + u"[I]: 初始化成功！")
        # 将stop_talking话题与回调函数绑定
        self.end_of_conv = self.Memory.subscriber("stop_talking")
        self.end_of_conv.signal.connect(self.callback_stoptalking)
        # 指示可以开始对话
        self.TextToSpeech.say("Talk to me please")
        time.sleep(0.5)

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头
        print(Fore.GREEN + u"[I]: 取消自主模式中")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        # 取消了自主模式，机器人会低头，通过站立初始化让机器人抬起头
        self.RobotPosture.goToPosture("StandInit", 0.5)

    def callback_stoptalking(self,msg):
        self.Dialog.unsubscribe('Talking')
        self.Dialog.deactivateTopic(self.topic_name)
        self.TextToSpeech.say("I heard stop, Thank you")
        self.switch = True

    def set_parameter(self):
        # 将机器人的语音设置为英文，设置机器人语音的速度
        self.TextToSpeech.setParameter("speed", 75.0)
        self.TextToSpeech.setLanguage("English")
        self.Dialog.setLanguage("English")

    def get_service(self, qiApp):
        # 获取本次案例中需要的服务
        self.TextToSpeech = qiApp.session.service("ALTextToSpeech")
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")
        self.Dialog = qiApp.session.service("ALDialog")
        self.Memory = qiApp.session.service("ALMemory")
        self.RobotPosture = qiApp.session.service("ALRobotPosture")

    def run(self):
        # 确保程序持续运行一段时间后能够停下来，并且取消对话引擎
        time.sleep(15)
        if self.switch == False:
            self.Dialog.unsubscribe('Talking')
            self.Dialog.deactivateTopic(self.topic_name)
            self.TextToSpeech.say("Thank you")

    def __del__(self):
        print(Fore.GREEN + u"[I]: 程序运行结束")

if __name__ == "__main__":
    dialog_intance = dialog()