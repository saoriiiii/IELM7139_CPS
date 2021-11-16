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
    global ori_z #added for test
    # position information
    x_value = msg.pose.pose.position.x
    y_value = msg.pose.pose.position.y

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

    #other parameters set
    cumulative_distance = 0
    range_value_last = range_value
    time_period = 0.2
    t = 0.0
    forward = True
    t_lasttime = rospy.get_time()


    while not rospy.is_shutdown():

        twist = Twist()

	#Turn around to the goal
        msg.linear.x = 0
        theta_angular = math.atan2(goal_y - y_value, goal_x - x_value) - yaw
        twist.angular.z = theta_angular
        print('theta_angular:', theta_angular)
        pub.publish(twist)
        pub.publish(msg)

        #The robot moves forward until it detects objects as close as 0.4m
        while range_value < 0.4:

	    print('nowfirstwhile')
            #To calculate duration to go forward after changing the angle
            begin_time_sec = rospy.get_time()
            now_time_sec = begin_time_sec

            msg.linear.x = 0
            twist.angular.z = -0.5
            pub.publish(twist)
            pub.publish(msg)

            #Robot will try to head for the goal when the robot is away from the obstacle when it rotates or it counts 2 seconds
            while (range_value >= 0.4) and (now_time_sec - begin_time_sec < 2):
                msg.linear.x = 0.5
	        now_time_sec = rospy.get_time()
	        pub.publish(msg)
	        print('nowtime:', now_time_sec,'begintime:', begin_time_sec)  
		break

        else:
            #When there is over 0.4m left to the object, move forward
	    print('else')
            msg.linear.x = 0.5
            x_linear = msg.linear.x
	    pub.publish(msg)

        print(yaw, x_value, y_value, ori_z)
        pub.publish(twist)
        pub.publish(msg)

        #ToDo
        #code something

    rospy.spin()

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass


