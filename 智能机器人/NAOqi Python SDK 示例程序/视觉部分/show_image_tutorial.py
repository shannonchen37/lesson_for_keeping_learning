#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
"""
代码名称：face_detection_tutorial.py
代码功能：检验Pepper机器人人脸检测功能
黑胡椒机器人技术有限公司开发
"""
import qi
import os
import sys
from colorama import init
init(autoreset=True)


class show_image:
    def __init__(self):
        qiApp = qi.Application(sys.argv)
        qiApp.start()
        self.get_service(qiApp)
        # 将展示图片写作类内函数，更方便调用
        self.show_image()
        qiApp.stop()

    def get_service(self, qiApp):
        # 声明需要使用的服务
        self.TabletService = qiApp.session.service("ALTabletService")

    def show_image(self):
        # 将需要展示的图片传输到机器人身上
        cmd = "sshpass -p nao scp ./pictures/image_sample.png nao@pepper.local:~/.local/share/PackageManager/apps/boot-config/html"
        os.system(cmd)
        self.TabletService.hideImage()
        self.TabletService.showImageNoCache("http://198.18.0.1/apps/boot-config/image_sample.png")

    def __del__(self):
        print(Fore.GREEN + u"[I]: 程序运行结束")

if __name__ == "__main__":
    show_image_intance = show_image()
