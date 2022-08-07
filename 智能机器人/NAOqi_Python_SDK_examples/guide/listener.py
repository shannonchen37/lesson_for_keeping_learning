#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

def listener():
    # "anonymous=True"保证在重名的节点时仍可以运行
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('chatter', String, callback)
    #保证程序一直在运行，直到节点被关闭程序才停止
    rospy.spin()

if __name__ == '__main__':
    listener()
