#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from random import randint
from std_msgs.msg import String

class Generator:
	def __init__(self):
		rospy.init_node("encoder_pub_node")

		self.pub_16 = rospy.Publisher('/serial/drive', String, queue_size = 10)
		self.pub_24 = rospy.Publisher('/serial/robotic_arm', String, queue_size = 10)

		self.continuous_gen()

	def random_gen_16(self):
		result_str = "A"

		for i in range(4):
			data = randint(-280, 280)
			print(data)
			sign = 1 if data < 0 else 0
			new_str = "{}{:03}".format(str(sign), abs(data))
			result_str = "{}{}".format(result_str, new_str)

		result_str = "{}{}".format(result_str, "B")

		return result_str

	def random_gen_24(self):	
		result_str = "A"

		for i in range(6):
			data = randint(-280, 280)
			print(data)
			sign = 1 if data < 0 else 0
			new_str = "{}{:03}".format(str(sign), abs(data))
			result_str = "{}{}".format(result_str, new_str)

		result_str = "{}{}".format(result_str, "B")

		return result_str

	def random_false_16(self):
		chars = "ABCDEFGH"
		index1, index2 = randint(0, 7), randint(0, 7)

		result_str = chars[index1]

		for i in range(4):
			data = randint(-280, 280)
			print(data)
			sign = 1 if data < 0 else 0
			new_str = "{}{:03}".format(str(sign), abs(data))
			result_str = "{}{}".format(result_str, new_str)

		result_str = "{}{}".format(result_str, chars[index2])

		return result_str

	def random_false_24(self):
		chars = "ABCDEFGH"
		index1, index2 = randint(0, 7), randint(0, 7)

		result_str = chars[index1]

		for i in range(6):
			data = randint(-280, 280)
			print(data)
			sign = 1 if data < 0 else 0
			new_str = "{}{:03}".format(str(sign), abs(data))
			result_str = "{}{}".format(result_str, new_str)

		result_str = "{}{}".format(result_str, chars[index2])

		return result_str

	def random_gen(self):
		len_chooser = randint(0, 1)
		gen_chooser = randint(0, 1)

		if len_chooser == 0: #16
			if gen_chooser == 0: #true
				data = self.random_gen_16()
			else:
				data = self.random_false_16()
			self.pub_16.publish(data)

		else: #24
			if gen_chooser == 0: #true
				data = self.random_gen_24()
			else:
				data = self.random_false_24()
			self.pub_24.publish(data)

	def continuous_gen(self):
		rate = rospy.Rate(1)

		while not rospy.is_shutdown():
			self.random_gen()
			rate.sleep()

		rospy.spin()

if __name__ == '__main__':
	g = Generator()