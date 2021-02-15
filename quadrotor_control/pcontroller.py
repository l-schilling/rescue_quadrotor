#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from math import *

class controller():
	def __init__(self):
		rospy.init_node('p2p_controller')
		self.pose_subscriber = rospy.Subscriber('/ground_truth_to_tf/pose', PoseStamped, self.update_pose)
		self.velo_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		self.pose_stamped = PoseStamped()
		self.rate = rospy.Rate(10)
	def update_pose(self, data):
		self.pose_stamped = data
	# def distance(self, goal_pose):
	# 	return sqrt((self.pose.position.x - goal_pose.pose.position.x)**2 + (self.pose.position.y - goal_pose.pose.position.y)**2)
	def control_law(self, goal_pose):
		kpose = 5.5
		ux = kpose * (goal_pose.pose.position.x - self.pose_stamped.pose.position.x)	
		uy = kpose * (goal_pose.pose.position.y - self.pose_stamped.pose.position.y)	
		uz = kpose * (goal_pose.pose.position.z - self.pose_stamped.pose.position.z)			
		# theta_r = atan2(uy,ux)		
		
		# v = sqrt(ux**2 + uy**2)
		# kangle = 0.6
		# w = kangle * (theta_r - self.pose.theta)
		w=0
		# Saturation
		vmax = 1.0 
		ux = max(-vmax,min(ux,vmax))
		uy = max(-vmax,min(uy,vmax))
		uz = max(-vmax,min(uz,vmax))

		return ux,uy,uz
	def move2goal(self):
		goal_pose = PoseStamped()
		goal_pose.pose.position.x = input("Set your x goal:")
		goal_pose.pose.position.y = input("Set your y goal:")
		goal_pose.pose.position.z = input("Set your z goal:")
		# distance_tolerance = input("Set your tolerance: ")

		vel_msg = Twist()
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		# while (self.distance(goal_pose) > distance_tolerance) and not rospy.is_shutdown():
		while not rospy.is_shutdown():
			# print "x:", self.pose.position.x, "y:", self.pose.position.y
			ux,uy,uz = self.control_law(goal_pose)
			vel_msg.linear.x = ux
			vel_msg.linear.y = uy
			vel_msg.linear.z = uz
			# vel_msg.angular.z = w
			self.velo_publisher.publish(vel_msg)
			self.rate.sleep()
		print "Reached the goal!"		
		vel_msg.linear.x = 0
		vel_msg.angular.z = 0
		self.velo_publisher.publish(vel_msg)
		rospy.spin()

if __name__ == '__main__':	
	try:
		x = controller()
		rospy.sleep(1) # waiting for the initial pose update
		x.move2goal()
	except rospy.ROSInterruptException: pass
