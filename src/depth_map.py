import numpy as np
import rospy
import cv2
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

cap1 = cv2.VideoCapture('rgb_comp3.avi')
cap=cv2.VideoCapture('depth_comp3.avi')

class DepthMap:
    def __init__(self):
        self.bridge = CvBridge()
        self.sub = rospy.Subscriber("/bot/camera/image_raw", Image, self.callback)
        self.cnt = 0

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "passthrough")
            self.perform(cv_image)
        except CvBridgeError as e:
            print(e)

    def perform(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray[np.where(gray < (np.min(gray) + 100))]=0

        gray_r=cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        print(gray.shape)
        #gray.resize(240,320)
        y=np.where(gray>gray.max()-50)

        if(self.cnt<5):
            u=np.random.normal(150,1,(gray.shape[0],gray.shape[1]))
            self.cnt+=self.cnt+1

        gray[y]=u[y]
        gray_r = cv2.GaussianBlur(gray_r, (7,7),0)
        mask=np.zeros_like(gray)
        thresh = cv2.threshold(gray_r, 0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        thresh=cv2.Canny(gray_r,0,255)
        #thresh=cv2.erode(thresh,(11,11),iterations=10)

        #thresh=cv2.dilate(thresh,(11,11),iterations=10)
        #thresh=cv2.Canny(thresh,l,h)
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            epsilon = 1*cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,epsilon,True)
            cv2.drawContours(mask, c, -1, (255),7)
            cv2.fillPoly(mask, pts=c,color=255)

        gray=np.where(mask==255, gray_r, gray)
        clr=cv2.applyColorMap(gray, cv2.COLORMAP_AUTUMN)
        cv2.imshow("o",clr)

if __name__=='__main__':
    rospy.init_node('depth_map')
    depthMap = DepthMap()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()
