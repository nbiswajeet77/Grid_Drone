import rospy
from std_msgs.msg import Header
from geometry_msgs.msg import Pose

from hector_uav_msgs.msg import PoseActionGoal

class Drone:
    def __init__(self):
        self.pub = rospy.Publisher('/action/pose/goal', PoseActionGoal, queue_size=10)
        self.publish()

    def position(self, target_pose):
		pose = Pose()
		pose.position.x = target_pose[0]
		pose.position.y = target_pose[1]
		pose.position.z = target_pose[2]
		pose.orientation.x = 0.0
		pose.orientation.y = 0.0
		pose.orientation.z = 0.0
		pose.orientation.w = 0.0
		return pose

    def publish(self):
        stamp = rospy.Time.now()
        header = Header()
        header.seq = 0
        header.frame_id = 'world'
        header.stamp = stamp
        pose = self.position([1,2,3,0,0,0])
        goal = PoseActionGoal()
        goal.header = header
        goal.goal_id.stamp = stamp
        goal.goal_id.id = '0'
        goal.goal.target_pose.header = header
        goal.goal.target_pose.pose = pose
        key=input('e')
        self.pub.publish(goal)

if __name__ == '__main__':
    rospy.init_node('grid_drone')
    drone = Drone()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print('shutting down')
