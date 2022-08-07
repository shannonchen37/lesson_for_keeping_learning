#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
import rospy
from sensor_msgs.msg import CameraInfo, Image


class pub_camera_info():
    def __init__(self):
        rospy.init_node("pub_camera_info")
        self.if_pub_angle = True
        self.info_sub = rospy.Subscriber("/pepper_robot/naoqi_driver/camera/ir/camera_info", CameraInfo, self.cmd_callback)
        self.image_sub = rospy.Subscriber("/pepper_robot/naoqi_driver/camera/ir/image_raw", Image, self.image_callback)
        self.info_pub = rospy.Publisher("/depth/camera_info", CameraInfo, queue_size=15)
        self.image_pub = rospy.Publisher("/depth/image_raw", Image, queue_size=15)
        self.Camera_info = CameraInfo()
        self.Image = Image()
        self.if_pub_info = False
        self.if_pub_image = False
        while not rospy.is_shutdown():
            if self.if_pub_info:
                self.info_pub.publish(self.Camera_info)
            if self.if_pub_image:
                self.image_pub.publish(self.Image)
            rospy.sleep(.3)

    def cmd_callback(self, msg):
        self.if_pub_info = True
        self.Camera_info = msg
        self.Camera_info.D = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.Camera_info.distortion_model = "plumb_bob"
        # self.info_sub.unregister()

    def image_callback(self, msg):
        self.Image = msg
        self.if_pub_image = True

if __name__ == '__main__':
    pub_camera_info()
