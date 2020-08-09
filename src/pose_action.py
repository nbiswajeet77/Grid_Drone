#!/usr/bin/env python
import rospkg
import rospy
from hector_uav_msgs.msg import PoseActionGoal, PoseActionResult
from hector_uav_msgs.srv import EnableMotors

from std_msgs.msg import Header
from geometry_msgs.msg import Pose, Twist
import csv

"""
Header header
actionlib_msgs/GoalID goal_id
PoseGoal goal ---> geometry_msgs/PoseStamped target_pose
"""

class PoseAction:
	def __init__(self):
		self.pub = rospy.Publisher('/action/pose/goal', PoseActionGoal, queue_size=1)
		self.sub = rospy.Subscriber('/action/pose/result', PoseActionResult, self.callback)
		self.rate = rospy.Rate(1)

		self.csv_data = []
		self.rospack = rospkg.RosPack()
		self.path = self.rospack.get_path('drone')
		print(self.enable_motors())
		self.read_csv()
		self.set_twist_limit()
		self.goal_gen(self.csv_data[0])

	def callback(self, result):
		id = int(result.status.goal_id.id)
		status = int(result.status.status)
		print(id, status)

		if (id < len(self.csv_data) - 1):
			row = self.csv_data[id + 1]
			self.goal_gen(row, id + 1)


	def enable_motors(self):
		rospy.wait_for_service('enable_motors')
		try:
			client = rospy.ServiceProxy('enable_motors', EnableMotors)
			result = client(True)
			return result
		except rospy.ServiceException as e:
			print("Service call failed: %s"%e)

	def set_twist_limit(self):
		pub = rospy.Publisher('/command/twist_limit', Twist, queue_size=10)
		twist = Twist()
		twist.linear.x = 0.6
		twist.linear.y = 0.4
		twist.linear.z = 0.7
		while pub.get_num_connections() < 1:
			pass
		pub.publish(twist)

	def read_csv(self):
		with open(self.path+'/src/position.csv', 'r') as file:
			data = csv.reader(file)
			for row in data:
				if len(row) < 7:
					continue
				row = [float(r) for r in row]
				self.csv_data.append(row)

	def pose_gen(self, target_pose):
		pose = Pose()
		pose.position.x = target_pose[0]
		pose.position.y = target_pose[1]
		pose.position.z = target_pose[2]
		pose.orientation.x = target_pose[3]
		pose.orientation.y = target_pose[4]
		pose.orientation.z = target_pose[5]
		pose.orientation.w = target_pose[6]
		return pose

	def goal_gen(self, col, id = 0):
		stamp = rospy.Time.now()
		header = Header()
		header.seq = id
		header.frame_id = 'world'
		header.stamp = stamp

		pose = self.pose_gen(col)

		goal = PoseActionGoal()
		goal.header = header
		goal.goal_id.stamp = stamp
		goal.goal_id.id = str(id)
		goal.goal.target_pose.header = header
		goal.goal.target_pose.pose = pose
		while self.pub.get_num_connections() < 1:
			pass
		self.pub.publish(goal)

if __name__ == '__main__':
	rospy.init_node('grid_drone')
	poseAction = PoseAction()
	try:
		rospy.spin()
	except rospy.ROSInterruptException as e:
		print(e)
