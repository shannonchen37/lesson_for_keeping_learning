#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
代码名称：audio_record.py
代码功能：此程序主要用于演示如何使用NAOqi的SDK进行音频录制
黑胡椒机器人技术有限公司开发
"""
import qi
import os
from threading import Thread
import time
from colorama import init, Fore
init(autoreset=True)


class event_test():
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        self.record_delay = 2.5
        self.record_time = 0.0
        self.enable_speech_recog = True
        self.audio_terminate = False
        self.get_service(qiApp)
        self.disable_auto_mode()
        self.set_parameter()
        self.start_sound_detection()
        self.start_audio_record()
        qiApp.stop()

    def get_service(self, qiApp):
        # 获取本次案例中需要的服务
        self.Memory = qiApp.session.service("ALMemory")
        self.Leds = qiApp.session.service("ALLeds")
        self.RobotPosture = qiApp.session.service("ALRobotPosture")
        self.AudioPlayer = qiApp.session.service("ALAudioPlayer")
        self.AudioRecorder = qiApp.session.service("ALAudioRecorder")
        self.SoundDetection = qiApp.session.service("ALSoundDetection")
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头，取消自主模式后重新站好
        print(Fore.GREEN + u"[I]: 取消自主模式中")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        self.RobotPosture.goToPosture("StandInit", 0.5)

    def set_parameter(self):
        # 声音检测
        self.SoundDetection.setParameter("Sensitivity", .3)

    def start_sound_detection(self):
        self.SoundDetection.subscribe('sd')
        # 声音检测的回调函数
        self.SoundDet_sub = self.Memory.subscriber("SoundDetected")
        self.SoundDet_sub.signal.connect(self.callback_sound_detected)

    def start_audio_record(self):
        # 录音的函数
        self.thread_recording = Thread(target=self.record_audio, args=(None,))
        self.thread_recording.daemon = True
        self.start_recording(reset=True)

    def __del__(self):
        print (Fore.GREEN + u"[I]: 退出程序中……")
        self.AudioRecorder.stopMicrophonesRecording()

    def callback_sound_detected(self, msg):
        if self.if_need_record:
            print (Fore.GREEN + u"[I]: 检测到声音（目前位于回调函数中）")
            ox = 0
            # 每次检测到声音，就在当前的时间节点往后录制3s
            for i in range(len(msg)):
                if msg[i][1] == 1:
                    ox = 1
            if ox == 1 and self.enable_speech_recog:
                self.record_time = time.time() + self.record_delay
            else:
                return None
        else:
            print (Fore.GREEN + u"[I]: 检测到声音，但是现在不需要录音")

    def kill_recording_thread(self):
        # 关掉录音的进程
        if self.thread_recording.is_alive():
            self.audio_terminate = True
            self.if_need_record = False

    def record_audio(self, withBeep = True):
        # 录音的函数
        # 亮眼部的灯
        self.Leds.on("FaceLeds")
        if withBeep:
            # 参数 playSine(频率, 音量, pan, 间隔)
            self.AudioPlayer.playSine(1000, 70, 1, .3)
        print(Fore.GREEN + u"[I]: 开始录音")
        channels = [1, 1, 1, 1]
        # 开始录音
        self.AudioRecorder.startMicrophonesRecording("/home/nao/audio/recog.wav", "wav", 16000, channels)
        # 持续的时间
        while time.time() < self.record_time:
            if self.audio_terminate:
                # 如果终止为True
                self.AudioRecorder.stopMicrophonesRecording()
                print(Fore.GREEN + u"[I]: 正在结束录音")
                return None
            time.sleep(.1)
        self.Leds.off("FaceLeds")
        self.AudioRecorder.stopMicrophonesRecording()
        if not os.path.exists("./audio"):
            os.mkdir('./audio', 0o755)
        # 复制录下的音频到自己的电脑上
        cmd = "sshpass -p nao scp nao@pepper.local:/home/nao/audio/recog.wav ./audio"
        os.system(cmd)
        print(Fore.GREEN + u"[I]: 录音结束")

    # 开始录音
    def start_recording(self, reset=False, base_duration=3, withBeep=True):
        self.if_need_record = True
        self.record_time = time.time() + base_duration
        # 如果当前有录音的线程在运行，就先把当前的线程退出
        if reset:
            self.kill_recording_thread()
            self.AudioRecorder.stopMicrophonesRecording()
        if not self.thread_recording.is_alive():
            # 开启一个线程进行录音
            self.thread_recording = Thread(target=self.record_audio, args=([withBeep]))
            self.thread_recording.daemon = False
            self.thread_recording.start()
            self.thread_recording.join()
            print(Fore.GREEN + u"[I]: 开启录音线程")


if __name__ == "__main__":
    event_test()
