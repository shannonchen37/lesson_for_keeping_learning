#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
代码名称：navigation_tutorial.py
代码功能：利用ROS实现Pepper机器人的定点导航以及键盘控制机器人行进
说明：此处提供的完整功能的代码为我们针对RoboCup@home中 Find my mates项目进行开发的示例，
      仅用来给Pepper初学者提供如何将各个功能综合起来的思路。综合示例涉及到Web API，Dlib库等，
      完整运行代码需要先配置好自己电脑的环境以及申请Web API的应用。
黑胡椒机器人技术有限公司开发
1. 修改sshpass的密码
2. 修改照片的路径
"""
import qi
import os
import re
import cv2
import dlib
import time
import rospy
import thread
import actionlib
import numpy as np
from colorama import Fore,init
from threading import Thread
from std_srvs.srv import Empty
from tf import transformations
from actionlib_msgs.msg import GoalID
from gender_predict import face_feature, body_feature
from speech_recog import baidu_recognition_text
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, PoseStamped, PoseWithCovarianceStamped, Quaternion
init(autoreset=True)


class find_my_mate():
    def __init__(self):
        qiApp = qi.Application()
        qiApp.start()
        self.get_service(qiApp)
        self.ros_init()
        self.disable_auto_mode()
        self.sound_record_init()
        self.Led_Tablet_init()
        # 声明需要的变量
        self.declare_variables()
        # 人脸识别
        self.detector = dlib.get_frontal_face_detector()
        # 调用成员函数
        self.start_head_fix()
        self.set_volume(.7)
        self.show_image("instructions.png")
        self.keyboard_control()
        self.__del__()
        qiApp.stop()

    def get_service(self, qiApp):
        self.Leds = qiApp.session.service("ALLeds")
        self.Memory = qiApp.session.service("ALMemory")
        self.Motion = qiApp.session.service("ALMotion")
        self.AudioPlayer = qiApp.session.service("ALAudioPlayer")
        self.PhotoCapture = qiApp.session.service("ALPhotoCapture")
        self.VideoDevice = qiApp.session.service("ALVideoDevice")
        self.RobotPosture = qiApp.session.service("ALRobotPosture")
        self.TextToSpeech = qiApp.session.service("ALTextToSpeech")
        self.AudioRecorder = qiApp.session.service("ALAudioRecorder")
        self.TabletService = qiApp.session.service("ALTabletService")
        self.SoundDetection = qiApp.session.service("ALSoundDetection")
        self.AutonomousLife = qiApp.session.service("ALAutonomousLife")

    def __del__(self):
        print (Fore.GREEN + u'[I]: 退出程序中... ')
        self.AudioRecorder.stopMicrophonesRecording()
        cv2.destroyAllWindows()

    def declare_variables(self):
        # 接近人脸的次数
        self.temp_reach_time = 0
        self.if_door_open = False
        self.position_result = []
        self.get_image_switch = True
        self.to_find_person_name = []
        # 保存当前对话人的年龄性别
        self.gender = "none"
        self.age = "none"
        # 储存每次语音识别的结果
        self.audio_recog_result = "none"
        # 保存当前人的肤色，衣服颜色和类别
        self.lower_color = "none"
        self.lower_wear = "none"
        self.upper_color = "none"
        self.upper_wear = "none"
        self.skin_color = "none"
        # 保存当前人旁边有什么东西
        self.position = "none"
        self.name_list = ["Max", "Alex", "Charlie", "Elizabeth", "Francis", "James", "Jennifer", "John", "Linda",
                          "Michael", "Mary", "Robert", "Patricia", "Robin", "Skyler", "William"]
        self.angle = -.1
        self.person_num = 1
        self.head_fix = True
        self.if_need_record = False
        # 录下的音频保存的路径
        self.audio_path = '/home/nao/audio/record.wav'
        self.recog_result = "00"
        # Beep 音量
        self.beep_volume = 70
        # 脸最大的人的中心
        self.center = 0

    def disable_auto_mode(self):
        # 取消机器人的自主模式，让机器人不会随着人转头，取消自主模式后重新站好
        print(Fore.GREEN + u"[I]: 取消自主模式中")
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        self.RobotPosture.goToPosture("StandInit", 0.5)

    def Led_Tablet_init(self):
        # LED的group
        self.led_name = ["Face/Led/Green/Right/0Deg/Actuator/Value", "Face/Led/Green/Right/45Deg/Actuator/Value",
                         "Face/Led/Green/Right/90Deg/Actuator/Value", "Face/Led/Green/Right/135Deg/Actuator/Value",
                         "Face/Led/Green/Right/180Deg/Actuator/Value", "Face/Led/Green/Right/225Deg/Actuator/Value",
                         "Face/Led/Green/Right/270Deg/Actuator/Value", "Face/Led/Green/Right/315Deg/Actuator/Value",
                         "Face/Led/Green/Left/0Deg/Actuator/Value", "Face/Led/Green/Left/45Deg/Actuator/Value",
                         "Face/Led/Green/Left/90Deg/Actuator/Value", "Face/Led/Green/Left/135Deg/Actuator/Value",
                         "Face/Led/Green/Left/180Deg/Actuator/Value", "Face/Led/Green/Left/225Deg/Actuator/Value",
                         "Face/Led/Green/Left/270Deg/Actuator/Value", "Face/Led/Green/Left/315Deg/Actuator/Value"]
        self.Leds.createGroup("MyGroup", self.led_name)
        # 初始化平板
        self.TabletService.hideImage()
        print (Fore.GREEN + u"[I]: 平板与LED初始化成功")

    def sound_record_init(self):
        # 检测上次是否未停止录音
        try:
            self.AudioRecorder.stopMicrophonesRecording()
        except BaseException as e:
            print(Fore.YELLOW + u"[W]: 当前无需停止录音")
        # 录音的函数
        self.thread_recording = Thread(target=self.record_audio, args=(None,))
        self.thread_recording.daemon = True
        self.audio_terminate = False
        # 初始化录音
        self.record_delay = 2.5
        self.speech_hints = []
        self.enable_speech_recog = True
        # 设置声音检测的参数
        self.SoundDetection.setParameter("Sensitivity", .4)
        self.SoundDetection.subscribe('sd')
        self.SoundDet_s = self.Memory.subscriber("SoundDetected")
        self.SoundDet_s.signal.connect(self.callback_sound_det)
        # 设置说话速度
        self.TextToSpeech.setParameter("speed", 75.0)
        self.TextToSpeech.setLanguage("English")
        print (Fore.GREEN + u'[I]: 语音部分初始化成功')

    def ros_init(self):
        rospy.init_node("find_my_mate")
        self.car_pose = MoveBaseGoal()
        # ROS 订阅器和发布器
        self.nav_as = actionlib.SimpleActionClient("/move_base", MoveBaseAction)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.goal_cancel_pub = rospy.Publisher('/move_base/cancel', GoalID, queue_size=1)
        self.nav_as.wait_for_server()
        # 清除costmap
        self.map_clear_srv = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
        self.map_clear_srv()
        self.Motion.setTangentialSecurityDistance(.05)
        self.Motion.setOrthogonalSecurityDistance(.1)
        # amcl_pose话题的订阅器
        self.amcl_pose_sb = None
        # 从文件中加载waypoints
        self.point_dataset = self.load_waypoint("waypoints.txt")
        self.predefined_position = {
                "trash bin":[4.34827899933, .21289503574, 0.0, 0.0, 0.932419364911, 0.361378095543],
                "tv":[6.94088697433, 2.1938290596, 0.0, 0.0, 0.387483707115, 0.921876551779],
                "couch":[6.29112815857, -0.861555457115, 0.0, 0.0, -0.27312959294, 0.961977247891],
                "arm chair":[7.84281349182, 0.143020510674, 0.0, 0.0, -0.401161409027, 0.916007382016]
            }
        print (Fore.GREEN + u'[I]: ROS初始化成功')

    def start_head_fix(self):
        arg = tuple([1])
        thread.start_new_thread(self.head_fix_thread, arg)

    def show_image(self, image_name):
        self.TabletService.hideImage()
        self.TabletService.showImage("http://198.18.0.1/apps/boot-config/" + str(image_name))

    def head_fix_thread(self, arg):
        self.Motion.setStiffnesses("head", 1.0)
        while True:
            if self.head_fix:
                self.Motion.setAngles("Head", [0., self.angle], .2)
            time.sleep(3)

    def say(self, text):
        self.TextToSpeech.say(text)

    def load_waypoint(self, file_name):
        curr_pos = PoseStamped()
        f = open(file_name, 'r')
        lines = f.readlines()
        points = {}
        for line in lines:
            temp1 = line.strip('\n')
            temp2 = temp1.split(',')
            point_temp = MoveBaseGoal()
            point_temp.target_pose.header.frame_id = '/map'
            point_temp.target_pose.header.stamp = curr_pos.header.stamp
            point_temp.target_pose.header.seq = curr_pos.header.seq
            point_temp.target_pose.pose.position.x = float(temp2[1])
            point_temp.target_pose.pose.position.y = float(temp2[2])
            point_temp.target_pose.pose.position.z = float(temp2[3])
            point_temp.target_pose.pose.orientation.x = float(temp2[4])
            point_temp.target_pose.pose.orientation.y = float(temp2[5])
            point_temp.target_pose.pose.orientation.z = float(temp2[6])
            point_temp.target_pose.pose.orientation.w = float(temp2[7])
            points[temp2[0]] = point_temp
        print (u"↓↓↓↓↓↓↓↓↓↓↓↓point↓↓↓↓↓↓↓↓↓↓↓↓")
        print (points)
        print (u"↑↑↑↑↑↑↑↑↑↑↑↑point↑↑↑↑↑↑↑↑↑↑↑↑")
        print (Fore.GREEN + u'[I]: 位置点加载完成')
        return points

    def set_volume(self, volume):
        self.TextToSpeech.setVolume(volume)

    def callback_sound_det(self, msg):
        if self.if_need_record:
            print (Fore.GREEN + u'[I]: 检测到声音(位于回调函数中) ')
            ox = 0
            for i in range(len(msg)):
                if msg[i][1] == 1:
                    ox = 1
            if ox == 1 and self.enable_speech_recog:
                self.record_time = time.time() + self.record_delay
                while self.recog_result == "00":
                    time.sleep(1)
                    continue
            else:
                return None
        else:
            print (Fore.GREEN + u'[I]: 检测到声音，现在未进行录音动作 ')

    def cal_distance(self, position, orientation):
        goal = transformations.euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
        min_dis = 1000
        # 寻找距离最近的点
        for i in self.predefined_position.keys():
            dist = (self.predefined_position[i][0] - position[0])*(self.predefined_position[i][0] - position[0]) + \
                   (self.predefined_position[i][1] - position[1])*(self.predefined_position[i][1] - position[1])
            if dist < min_dis:
                temp = transformations.euler_from_quaternion(
                    [self.predefined_position[i][2], self.predefined_position[i][3],
                     self.predefined_position[i][4], self.predefined_position[i][5]])
                if (temp[2] > 0 and goal[2] > 0) or (temp[2] < 0 and goal[2] < 0):
                    if abs(temp[2] - goal[2]) > 2.8 / 2:
                        continue
                    else:
                        min_dis = dist
                        self.position = i
                elif temp[2] > 0 and goal[2] < 0 or temp[2] < 0 and goal[2] > 0:
                    if (6.28 - (abs(temp[2]) + abs(goal[2]))) < 2.8 / 2 or (abs(temp[2]) + abs(goal[2])) < 2.8 / 2:
                        min_dis = dist
                        self.position = i
                    else:
                        continue

    def analyze_content(self):
        result = []
        # 记录是否找到人
        person_found = False
        # 获取要找的人姓名
        for i in range(len(self.name_list)):
            if re.search(self.name_list[i].lower(), self.recog_result) != None:
                print (Fore.GREEN + (u'[I]: 找到的人：' + self.name_list[i].lower()))
                person_found = True
                # 记下当前人的名字
                result.append(self.name_list[i])
        self.recog_result = "00"
        if person_found:
            self.audio_recog_result = result
            return
        else:
            self.say("sorry, please tell me again")
            self.start_recording(reset=True)
            self.analyze_content()

    def start_recording(self, reset=False, base_duration=3, withBeep=True):
        self.if_need_record = True
        self.record_time = time.time() + base_duration
        if reset:
            self.kill_recording_thread()
            self.AudioRecorder.stopMicrophonesRecording()
        if not self.thread_recording.is_alive():
            self.thread_recording = Thread(target=self.record_audio, args=(self.speech_hints, withBeep))
            self.thread_recording.daemon = False
            self.thread_recording.start()
            self.thread_recording.join()
            print(Fore.GREEN + u'[I]: 开始录音的线程')

    def record_audio(self, hints, withBeep = True):
        # 亮灯
        self.Leds.on("MyGroup")
        if withBeep:
            # 参数 playSine(const int& frequence, const int& gain, const int& pan, const float& duration)
            self.AudioPlayer.playSine(1000, self.beep_volume, 1, .3)
        print(Fore.GREEN + u'[I]: 开始录音')
        channels = [0, 0, 1, 0]
        self.AudioRecorder.startMicrophonesRecording("/home/nao/audio/recog.wav", "wav", 16000, channels)
        while time.time() < self.record_time:
            if self.audio_terminate:
                # 如果终止为True
                self.AudioRecorder.stopMicrophonesRecording()
                return None
            time.sleep(.1)
        self.Leds.off("MyGroup")
        self.AudioRecorder.stopMicrophonesRecording()
        self.AudioRecorder.recording_ended = True
        if not os.path.exists('./audio_record'):
            os.mkdir('./audio_record', 0o755)
        # 复制录下的音频到自己的电脑上
        cmd = "sshpass -p xxxxx scp nao@pepper.local:/home/nao/audio/recog.wav ./audio_record"
        os.system(cmd)
        self.recog_result = baidu_recognition_text.main("./audio_record/recog.wav").lower()
        print (Fore.GREEN + (u'[I]: 识别结果为：' + self.recog_result))

    def take_picture(self):
        self.PhotoCapture.takePictures(3, '/home/nao/picture', 'party')
        cmd = "sshpass -p xxxxx scp nao@pepper.local:/home/nao/picture/party_0.jpg ./person_image"
        os.system(cmd)
        self.gender, self.age, self.skin_color = face_feature.gender("./person_image/party_0.jpg", self.upper_wear, self.upper_color, self.person_num)
        if self.gender == "none":
            self.say("please look at my eyes")
            self.take_picture()
        else:
            return self.gender

    def add_name_to_img(self, img_name, position, person_name, posture):
        img = cv2.imread(img_name)
        cv2.putText(img, "Name:"+str(person_name), (160, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.putText(img, "Position:"+posture+" next to the "+str(position), (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.imwrite(img_name, img)
        # 将当前人的信息传输到Pepper上
        cmd = "sshpass -p xxxxx scp ./person_result" + str(self.person_num) + \
              ".jpg nao@pepper.local:~/.local/share/PackageManager/apps/boot-config/html"
        os.system(cmd)

    def amcl_pose_cb(self, msg):
        qua = Quaternion()
        position = [msg.pose.pose.position.x, msg.pose.pose.position.y]
        qua.x = msg.pose.pose.orientation.x
        qua.y = msg.pose.pose.orientation.y
        qua.z = msg.pose.pose.orientation.z
        qua.w = msg.pose.pose.orientation.w
        self.cal_distance(position, qua)
        self.amcl_pose_sb.unregister()

    def save_point(self):
        self.if_save_switch = True
        # amcl定位
        amcl_sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.amcl_callback)
        while self.if_save_switch:
            time.sleep(1)
        amcl_sub.unregister()

    def laser_callback(self, msg):
        # 检测中间的laser的信息判断门是不是开着的
        dis_sum = 0
        num_laser = 0
        # 前面的laser的数据
        for i in range(23, 37):
            if msg.ranges[i] > 5:
                continue
            else:
                num_laser += 1
                dis_sum += msg.ranges[i]
        # 大于阈值就认定门开了
        print dis_sum / num_laser
        if dis_sum / num_laser > 1:
            self.if_door_open = True
            self.laser_sb.unregister()

    def amcl_callback(self, msg):
        point_temp = MoveBaseGoal()
        point_temp.target_pose.header.frame_id = '/map'
        point_temp.target_pose.header.stamp = msg.header.stamp
        point_temp.target_pose.header.seq = msg.header.seq
        point_temp.target_pose.pose.position.x = msg.pose.pose.position.x
        point_temp.target_pose.pose.position.y = msg.pose.pose.position.y
        point_temp.target_pose.pose.position.z = msg.pose.pose.position.z
        point_temp.target_pose.pose.orientation.x = msg.pose.pose.orientation.x
        point_temp.target_pose.pose.orientation.y = msg.pose.pose.orientation.y
        point_temp.target_pose.pose.orientation.z = msg.pose.pose.orientation.z
        point_temp.target_pose.pose.orientation.w = msg.pose.pose.orientation.w
        self.point_dataset["start"] = point_temp
        self.if_save_switch = False

    def start(self):
        # 开门进屋
        # 订阅laser的话题，判断门是不是开着的
        self.TextToSpeech.say("I am ready, please help me open the door.")
        self.laser_sb = rospy.Subscriber('/pepper_robot/laser', LaserScan, self.laser_callback)
        print (Fore.GREEN + u"[I]: 开始")
        while not self.if_door_open:
            time.sleep(.5)
        self.TextToSpeech.say("the door is open")
        self.map_clear_srv()
        time.sleep(1)
        self.go_to_waypoint(self.point_dataset["point0"])
        # 抬头
        self.angle = -.5
        self.save_point()
        self.Motion.setAngles("Head", [0., self.angle], .2)
        self.TextToSpeech.say("Dear operator.")
        self.TextToSpeech.say("Please talk to me after my eyes' color turn to white ")
        self.TextToSpeech.say("Please give me a name")
        time.sleep(1)
        self.to_find_person_name = ["test"]
        while True:
            # 开始和operator对话
            self.start_recording(reset=True)
            self.analyze_content()
            self.to_find_person_name = self.audio_recog_result
            break
        self.say("ok, I will find ")
        for i in range(len(self.to_find_person_name)):
            self.say(str(self.to_find_person_name[i]) + " ")
        self.TextToSpeech.say("excuse me, please let the way")
        self.map_clear_srv()
        time.sleep(2)
        # 走进屋子，开始找人
        self.go_to_waypoint(self.point_dataset["point1"])
        person_found_num = 0
        while person_found_num != len(self.to_find_person_name):
            self.find_person()
            self.get_image_switch = True
            self.amcl_pose_sb = rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, self.amcl_pose_cb)
            # 如果找到的人是我们的list的人
            if self.dialog_with_people() == "succe":
                person_found_num += 1
                self.Motion.moveTo(0, 0, 3.14 / 4)
                self.show_image("instructions.png")
            else:
                self.Motion.moveTo(0, 0, 3.14 / 4)
                self.show_image("instructions.png")
                continue
        # 回到operator那里
        self.Motion.moveTo(0, 0, 3)
        self.go_to_waypoint(self.point_dataset["point0"])
        self.angle = -.5
        for i in range(len(self.position_result)):
            image_name = "person_result"+str(i+1)+".jpg"
            self.show_image(image_name)
            self.say(self.position_result[i])

    def stop_motion(self):
        self.goal_cancel_pub.publish(GoalID())
        self.set_velocity(0, 0, 0)

    def dialog_with_people(self):
        # 抬头
        self.angle = -.5
        self.Motion.setAngles("Head", [0., self.angle], .1)
        time.sleep(1)
        # 拍照识别性别
        self.take_picture()
        self.show_image("instructions.png")
        self.say("Hi, my name is pepper, what is your name?")
        self.start_recording(reset=True)
        self.analyze_content()
        for i in range(len(self.to_find_person_name)):
            # 如果这个人在要找的list里面
            if re.search(self.audio_recog_result[0].lower(), self.to_find_person_name[i].lower()) != None:
                self.say("ok, I have remembered your position")
                if self.angle < -0.35:
                    posture = "standing"
                else:
                    posture = "sitting"
                self.add_name_to_img("person_result" + str(self.person_num) + ".jpg", self.position, self.to_find_person_name[i].lower(), posture)
                # num数加1
                self.person_num += 1
                if self.gender == "male":
                    sentence = "the person named " + self.to_find_person_name[i].lower() + " is " + self.gender + ". And he is wearing " + \
                               self.upper_color + " " + self.upper_wear + ". And he is "+ posture +" next to " + self.position
                else:
                    sentence = "the person named " + self.to_find_person_name[i].lower() + " is " + self.gender + ". And she is wearing " + \
                               self.upper_color + " " + self.upper_wear + ". And she is "+ posture +" next to " + self.position
                self.position_result.append(sentence)
                self.upper_color = self.upper_wear = self.lower_wear = self.lower_color = self.position = self.gender = "none"
                # 找到了我们要找的人，返回“succe”
                return "succe"
        self.TextToSpeech.say("ok, thank you")
        # 最终没有找到我们要的人，返回“wrong”
        return "wrong"

    def set_velocity(self, x, y, theta, duration=-1.):  # m/sec, rad/sec
        tt = Twist()
        tt.linear.x = x
        tt.linear.y = y
        tt.angular.z = theta
        self.cmd_vel_pub.publish(tt)
        if duration < 0: return None
        tic = time.time()
        while time.time() - tic < duration:
            self.cmd_vel_pub.publish(tt)
            time.sleep(0.1)
        tt = Twist()
        tt.linear.x = 0
        tt.linear.y = 0
        tt.angular.z = 0
        self.cmd_vel_pub.publish(tt)

    def kill_recording_thread(self):
        if self.thread_recording.is_alive():
            self.audio_terminate = True
            self.if_need_record = False

    def find_person(self):
        self.angle = -.2
        self.Motion.setAngles("Head", [0., self.angle], .2)
        AL_kQVGA = 2
        current_right = current_left = current_bottom = current_top = 0
        AL_kRGBColorSpace = 13
        fps = 60
        nameId = self.VideoDevice.subscribe("image" + str(time.time()), AL_kQVGA, AL_kRGBColorSpace, fps)
        # 创建一张等大小的图片
        width = 640
        height = 480
        image = np.zeros((height, width, 3), np.uint8)
        if_turn_finished = False
        if_first = True
        while self.get_image_switch:
            result = self.VideoDevice.getImageRemote(nameId)
            if result != None and result[6] != None:
                values = map(ord, list(str(bytearray(result[6]))))
                i = 0
                for y in range(0, height):
                    for x in range(0, width):
                        image.itemset((y, x, 0), values[i + 0])
                        image.itemset((y, x, 1), values[i + 1])
                        image.itemset((y, x, 2), values[i + 2])
                        i += 3
                cv2.imshow("pepper-top-camera-640*480px", image)
                cv2.waitKey(1)
                # dlib检测人脸
                rects = self.detector(image, 2)
                # 检测到人脸
                if len(rects) != 0:
                    if_first = True
                    # 转向完成，开始接近人
                    if if_turn_finished:
                        # 第一次看到人，就进行一次特征识别
                        if (self.upper_wear == "none" and self.upper_color == "none"):
                            image_name = "./person_body.jpg"
                            cv2.imwrite(image_name, image)
                            _, _, self.upper_color, self.upper_wear = body_feature.feature(image_name)
                            if self.upper_color == "none" and self.upper_wear == "none":
                                self.angle -= .05
                                self.Motion.setAngles("Head", [0., self.angle], .2)
                                continue
                        # 接近脸最大的那个人
                        image_max = 0
                        for rect in rects:
                            cv2.rectangle(image, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0, 0, 255), 2, 8)
                            cv2.imshow("yess", image)
                            cv2.imwrite("./person.jpg", image)
                            if (rect.right() - rect.left()) * (rect.bottom() - rect.top()) > image_max:
                                image_max = (rect.right() - rect.left()) * (rect.bottom() - rect.top())
                                current_bottom = rect.bottom()
                                current_top = rect.top()
                                current_left = rect.left()
                                current_right = rect.right()
                        if self.temp_reach_time == 15:
                            self.temp_reach_time = 0
                            self.set_velocity(0, 0, 0)
                            self.get_image_switch = False
                        if float(image_max) / float(width * height) > .04:
                            self.temp_reach_time = 0
                            self.set_velocity(0, 0, 0)
                            self.get_image_switch = False
                        else:
                            self.temp_reach_time += 1
                            # 判断是佛需要抬头
                            if current_bottom < height / 1.6:
                                self.angle -= .05
                                self.Motion.setAngles("Head", [0., self.angle], .2)
                            elif current_top > 1.2 * height / 1.6:
                                self.angle += .05
                                self.Motion.setAngles("Head", [0., self.angle], .2)
                            self.set_velocity(.15, 0, 0)
                            # 再旋转
                            center = (current_left + current_right) / 2
                            if abs(width / 2 - center) > width / 10:
                                Error_dist_ = width / 2 - center
                                self.set_velocity(0, 0, 0.001*Error_dist_)
                                time.sleep(1.8)
                                self.set_velocity(0.1, 0, 0)
                        cv2.waitKey(1)
                    # 开始转向人
                    else:
                        image_max = 0
                        for rect in rects:
                            cv2.rectangle(image, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0, 0, 255),
                                          2, 8)
                            cv2.imshow("yess", image)
                            cv2.imwrite("./person.jpg", image)
                            if (rect.right() - rect.left()) * (rect.bottom() - rect.top()) > image_max:
                                image_max = (rect.right() - rect.left()) * (rect.bottom() - rect.top())
                                self.center = (rect.left() + rect.right()) / 2
                        Error_dist = width / 2 - self.center
                        if abs(Error_dist) <= 30:
                            if_turn_finished = True
                            continue
                        self.Motion.moveTo(0, 0, 0.002*Error_dist)
                        cv2.waitKey(1)
                # 没有检测到人脸就旋转
                else:
                    if if_first:
                        if_first = False
                        continue
                    self.Motion.moveTo(0, 0, 3.14 / 4)
        return "succe"

    def go_to_waypoint(self, Point): # Point代表目标点 destination代表目标点的文本 label
        # 设置头的角度
        self.angle = .3
        self.Motion.setAngles("Head", [0., self.angle], .2)
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

    def keyboard_control(self):
        print (Fore.GREEN + u'[I]: 开始键盘控制')
        command = ''
        while command != 'c':
            try:
                command = raw_input('next command : ')
                if command == 'st':
                    self.start()
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
                elif command == 'c':
                    break
                else:
                    print(u"Invalid Command!")
            except Exception as e:
                print e

if __name__ == "__main__":
    find_my_mate()
