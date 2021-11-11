#!/usr/bin/env python
# license removed for brevity
import rospy
import numpy as numpy
import PyKDL
import math
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped

range_value = 0.0
x_value = 0.0
y_value = 0.0
yaw = 0.0

def callback(msg):
    global range_value
    range_value = msg.range

def posecallback(msg):
    global x_value, y_value, yaw
    # position information
    x_value = msg.pose.pose.orientation.x
    y_value = msg.pose.pose.orientation.y

    ori_x = msg.pose.pose.orientation.x
    ori_y = msg.pose.pose.orientation.y
    ori_z = msg.pose.pose.orientation.z
    ori_w = msg.pose.pose.orientation.w #what's w??
    rot = PyKDL.Rotation.Quaternion(ori_x, ori_y, ori_z, ori_w)
    # Orientation Information
    yaw = rot.GetRPY()[2]

def move():
    sub = rospy.Subscriber('//sonar_1', Range, callback)    # in real robot: /sonar
    amcl_sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, posecallback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('bug0', anonymous=True)
    rate = rospy.Rate(10)
    msg = Twist()
    global range_value
    rospy.Time.now()
    rospy.get_rostime()

    #goal position (fixed)
    goal_x = 1.8
    goal_y = 0.0

    cumulative_distance = 0
    range_value_last = range_value
    time_period = 0.2
    t = 0.0
    forward = True
    t_lasttime = rospy.get_time()

    #linear
    x_linear = msg.linear.x
    y_linear = msg.linear.y
    z_linear = msg.linear.z



    while not rospy.is_shutdown():

        #adjust timing to print
        t_now = rospy.get_rostime()
        msg.linear.x = x_linear + 0.1
        x_linear = msg.linear.x
	#y_linear = y_linear + 1
	print(x_linear, y_linear, z_linear)
        pub.publish(msg)

        #ToDo
        #code something

    rospy.spin()

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass


