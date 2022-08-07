#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
代码名称：navigation_tutorial.py
代码功能：利用ROS实现Pepper机器人的定点导航以及键盘控制机器人行进
黑胡椒机器人技术有限公司开发
"""
import qi
from std_srvs.srv import Empty
import rospy
import actionlib
import time
from colorama import init, Fore
from actionlib_msgs.msg import GoalID
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Twist
init(autoreset=True)


class event_test():
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        self.init_ros()
        self.get_service(qiApp)
        self.set_parameter()
        self.disable_auto_mode()
        dest_point = self.get_destination()
        self.go_to_waypoint(dest_point)
        qiApp.stop()

    def init_ros(self):
        # 声明一个ROS节点
        rospy.init_node("navigation")
        # 清除costmap
        self.map_clear_srv = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
        self.map_clear_srv()
        # ROS 订阅器和发布器
        self.nav_as = actionlib.SimpleActionClient("/move_base", MoveBaseAction)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.goal_cancel_pub = rospy.Publisher('/move_base/cancel', GoalID, queue_size=1)
        self.nav_as.wait_for_server()

    def get_service(self, qiApp):
        # 获取本次案例中需要的服务
        self.Memory = qiApp.session.service("ALMemory")
        self.Motion = qiApp.session.service("ALMotion")
        self.TextToSpeech = qiApp.session.service("ALTextToSpeech")
        self.RobotPosture = qiApp.session.service("ALRobotPosture")
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头，取消自主模式后重新站好
        print(Fore.GREEN + u"[I]: 取消自主模式中")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        self.RobotPosture.goToPosture("StandInit", 0.5)

    def set_parameter(self):
        # 设置语言
        self.TextToSpeech.setLanguage("Chinese")
        # 设置安全距离
        self.Motion.setTangentialSecurityDistance(.05)
        self.Motion.setOrthogonalSecurityDistance(.1)

    # 手动退出程序
    def keyboard_control(self):
        print(Fore.GREEN + u"[I]: 开始键盘控制")
        command = ''
        # 只有输入 c 的时候才会退出程序
        while command != 'c':
            try:
                command = raw_input('next command : ')
                if command == 'c':
                    break
                elif command == 'w':
                    self.set_velocity(0.25, 0, 0)
                elif command == 's':
                    self.stop_motion()
                elif command == 'x':
                    self.set_velocity(-0.25, 0, 0)
                elif command == 'a':
                    self.set_velocity(0, 0.25, 0)
                elif command == 'd':
                    self.set_velocity(0, -0.25, 0)
                elif command == 'q':
                    self.set_velocity(0, 0, 0.35)
                elif command == 'e':
                    self.set_velocity(0, 0, -0.35)
                else:
                    print(Fore.YELLOW + u"[W]: 输入了无效的指令。可以选择：w:前进 x:后退 a：左移 d：右移 q：左转 e：右转 x：停止")
            except Exception as e:
                print e

    # 前往目标点
    def go_to_waypoint(self, Point): # Point代表目标点 destination代表目标点的文本 label
        # 设置固定的头的角度
        self.angle = .3
        # 发送目标点
        self.nav_as.send_goal(Point)
        # 清空局部地图
        self.map_clear_srv()
        count_time = 0
        # 等于3的时候就是到达目的地了
        while self.nav_as.get_state() != 3:
            count_time += 1
            time.sleep(1)
            if count_time == 8:
                self.map_clear_srv()
                count_time = 0
        self.TextToSpeech.say("我到达了目标点")

    # 获取目标点
    def get_destination(self):
        point_temp = MoveBaseGoal()
        point_temp.target_pose.header.frame_id = '/map'
        point_temp.target_pose.pose.position.x = 1.99512815475
        point_temp.target_pose.pose.position.y = -0.992116451263
        point_temp.target_pose.pose.orientation.z = 0.00512512288357
        point_temp.target_pose.pose.orientation.w = 0.999986866471
        print (Fore.GREEN + u"[I]: 目标点已取得")
        return point_temp

    # 停止移动
    def stop_motion(self):
        self.goal_cancel_pub.publish(GoalID())
        self.set_velocity(0, 0, 0)

    # 设置移动的速度
    def set_velocity(self, x, y, theta, duration=-1.):  # m/sec, rad/sec
        tt = Twist()
        tt.linear.x = x
        tt.linear.y = y
        tt.angular.z = theta
        self.cmd_vel_pub.publish(tt)
        if duration < 0:
            return None
        tic = time.time()
        while time.time() - tic < duration:
            self.cmd_vel_pub.publish(tt)
            time.sleep(0.1)
        tt = Twist()
        tt.linear.x = 0
        tt.linear.y = 0
        tt.angular.z = 0
        self.cmd_vel_pub.publish(tt)

if __name__ == "__main__":
    event_test()
