#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String

def talker():
    # 初始化一个ROS节点
    rospy.init_node('talker', anonymous=True)
    # 声明一个发布器
    pub = rospy.Publisher('chatter', String, queue_size=10)
    # 设置一个频率 10Hz
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        # 输出信息到终端
        rospy.loginfo(hello_str)
        # 发布信息
        pub.publish(hello_str)
        # 按照规定的频率，停止一段时间
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
