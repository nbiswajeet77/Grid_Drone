#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
from nav_msgs.msg import Odometry
import struct
import csv

class Draw(object):
    def __init__(self):
        self.yellow = struct.unpack('I', struct.pack('BBBB', 0, 255, 255, 255))[0]
        self.green = struct.unpack('I', struct.pack('BBBB', 0, 255, 0, 255))[0]

        self.pub = rospy.Publisher("/draw", PointCloud2, queue_size=100)
        self.sub = rospy.Subscriber("/ground_truth/state", Odometry, self.callback)

        self.header = Header()
        self.header.frame_id = "world"
        self.fields = [ PointField('x', 0, PointField.FLOAT32, 1),
                        PointField('y', 4, PointField.FLOAT32, 1),
                        PointField('z', 8, PointField.FLOAT32, 1),
                        PointField('rgba', 12, PointField.UINT32, 1)]
        self.points = []
        self.gate = []
        self.read_csv()

    def callback(self, data):
        x, y = data.pose.pose.position.x, data.pose.pose.position.y
        for g in self.gate:
            # print(g[1], y, y-g[1])
            if y > g[1] - 3 and y < g[1] - 2.5:
                print(g[1], y, y-g[1]+3)
                self.points.append(g)
        self.draw()

    def read_csv(self):
        with open('position.csv', 'r') as file:
            data = csv.reader(file)
            row = []
            for r in data:
                row.append(r)
            for i in range(5, len(row), 3):
                x = float(row[i][0]) + float(row[i+1][0])
                y = float(row[i][1]) + float(row[i+1][1])
                z = float(row[i][2]) + float(row[i+1][2])
                color = self.green * np.ones([len(self.points), 1])
                self.gate.append([x/2, y/2, z/2, color])

    def draw(self):
        print(self.points)
        self.publish()
        # for i in range(len(self.var['x_mid'])):
        #     y_mid = -1 * self.var['x_mid'][i]
        #     x_mid = self.var['y_mid'][i]
        #
        #     d = np.sqrt(x_mid ** 2 + y_mid ** 2)
        #     lin = np.linspace(0, x_mid, d * 40)
        #     points = [[x, y_mid / x_mid * x, 0, self.yellow]  for x in lin]
        #     points.append([0,0,0,self.yellow])
        #     self.points = np.vstack((self.points, points))

    def publish(self):
        pc2 = point_cloud2.create_cloud(self.header, self.fields, self.points)
        pc2.header.stamp = rospy.Time.now()
        self.pub.publish(pc2)

if __name__ == '__main__':
    rospy.init_node('draw')
    d = Draw()
    try:
        rospy.spin()
    except ROSInterruptException as e:
        print(e)
