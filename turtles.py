#! /usr/bin/python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt

class Moving_Turtles:
	def __init__(self):
		self.r = rospy.Rate(50) #Hz
		rospy.Subscriber('/turtle1/pose', Pose, self.turtle1_callback)
		rospy.Subscriber('/beta/pose', Pose, self.beta_callback)
		self.pub_beta = rospy.Publisher('/beta/cmd_vel', Twist, queue_size = 1)
		self.pose = Pose()
		
	def turtle1_callback(self, msg):
		temp_pose = Pose()
		temp_pose.x = msg.x
		temp_pose.y = msg.y
		
		temp_msg = Twist()

		#rospy.loginfo(str("msg") + ' ' + str(msg.x) + ' ' + str(msg.y))
	
		while self.euclidean_distance(msg) >= 0.01 :
			temp_msg.linear.x = self.linear_vel(temp_pose)
			temp_msg.angular.z = self.angular_vel(temp_pose)
			#rospy.loginfo(str(temp_msg.linear.x) + ' ' + str(temp_msg.angular.z))
			self.pub_beta.publish(temp_msg)
			self.r.sleep()
		
	def beta_callback(self, msg):
		self.pose = msg
		self.pose.x = round(self.pose.x, 4)
		self.pose.y = round(self.pose.y, 4)
  
	def euclidean_distance(self, temp_pose):
		return sqrt(pow((temp_pose.x - self.pose.x), 2) +
                       pow((temp_pose.y - self.pose.y), 2))
  
	def linear_vel(self, temp_pose, constant=1.5):
		return constant * self.euclidean_distance(temp_pose)
  
	def steering_angle(self, temp_pose):
		return atan2(temp_pose.y - self.pose.y, temp_pose.x - self.pose.x)
  
	def angular_vel(self, temp_pose, constant=6):
		return constant * (self.steering_angle(temp_pose) - self.pose.theta)
		
rospy.init_node('init_node')
Moving_Turtles()
rospy.spin() 
