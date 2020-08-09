import rospy
from hector_uav_msgs.msg import PoseActionGoal, PoseActionResult
from std_msgs.msg import Header
from geometry_msgs.msg import Pose
import csv

"""
Header header
actionlib_msgs/GoalID goal_id
PoseGoal goal ---> geometry_msgs/PoseStamped target_pose
"""

def PoseResult(self, data):
		print(data.status.goal_id.id, data.status.status)


def PoseAction():
	pub = rospy.Publisher('/action/pose/goal', PoseActionGoal, queue_size=10)
	rospy.Subscriber('/action/pose/result', PoseActionResult, PoseResult)

	stamp = rospy.Time.now()
	goal = PoseActionGoal()
	header = Header()
	header.seq = 0
	header.stamp = stamp
	header.frame_id = 'world'
	pose = Pose()

	key = input('pose: ')

	if (key != None):
		pose.position.x = key[0]
		pose.position.y = key[1]
		pose.position.z = key[2]
		pose.orientation.x = 0
		pose.orientation.y = 0
		pose.orientation.z = 0
		pose.orientation.w = 0

		goal.header = header
		goal.goal_id.stamp = stamp
		goal.goal_id.id = str(key)
		goal.goal.target_pose.header = header
		goal.goal.target_pose.pose = pose

		pub.publish(goal)

if __name__ == '__main__':
	try:
		rospy.init_node('grid_test')
		PoseAction()
	except rospy.ROSInterruptException:
		psss
