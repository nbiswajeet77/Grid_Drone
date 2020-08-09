#!/usr/bin/env python
import numpy as np
import rospy
import cv2
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

class DepthMap:
    def __init__(self):
        self.bridge = CvBridge()
        self.sub1 = rospy.Subscriber("/image_view/output", Image, self.callback_depth)
        self.sub2 = rospy.Subscriber("/front_cam/camera/image", Image, self.callback_raw)
        raw_img = np.zeros((463, 485))

    def callback_raw(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.raw_img = cv2.resize(cv_image, (463, 485))
        except CvBridgeError as e:
            print(e)

    def callback_depth(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "passthrough")
            self.perform(cv_image)
        except CvBridgeError as e:
            print(e)

    def motion_blur(self, input, size=15):
        kernel_motion_blur = np.zeros((size, size))
        kernel_motion_blur[int((size-1)/2), :] = np.ones(size)
        kernel_motion_blur = kernel_motion_blur / size

        output = cv2.filter2D(input, -1, kernel_motion_blur)
        return output

    def perform(self, frame):
        gray = 255 - cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (463, 485))
        blur = self.motion_blur(gray)
                # blur = cv2.blur(blur, (5,5))
        map = cv2.applyColorMap(blur, cv2.COLORMAP_PINK)

        it = np.random.randint(1, 5)
        kernels = [1, 3, 5, 7, 9]
        k = kernels[it]
        map = cv2.erode(map,(k,k),iterations=it*2)
        it = np.random.randint(1, 4)
        k = kernels[it]
        map = cv2.dilate(map,(k,k),iterations=it*2)

        out = np.concatenate((self.raw_img,map),axis=1)
        cv2.imshow('frame', out)
        cv2.waitKey(10)

if __name__=='__main__':
    rospy.init_node('depth_map')
    depthMap = DepthMap()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()
