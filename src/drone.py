#!/usr/bin/env python
import numpy as np
import rospy
import cv2
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

class Drone:
    def __init__(self):
        self.bridge = CvBridge()
        self.sub = rospy.Subscriber("/image_view/output", Image, self.callback)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "passthrough")
            # cv2.imshow('image', cv_image)
            # cv2.waitKey(10)
            self.perform(cv_image)
        except CvBridgeError as e:
            print(e)

    def perform(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # print(gray.shape[0])
        gray = cv2.resize(gray, (463, 485))
        gray1=np.full_like(gray,255)
        gray2=gray1.copy()
        y=np.where(gray>gray.max()-20)

        #print(y)
        #gray[y]=np.random.randint(200,255,(len(y[0]),len(y[1])))
            #gray[y[0][i],y[1][i]]=0
        gray1=gray.copy()
        #gray1[125:470,10:630] = gray.copy()[125:470,10:630]
        img3=gray1
        img3[np.where(gray1 < (np.min(gray1) + 100))]=0
        img3[np.where(gray1>0)]=255
        img3=cv2.Canny(img3,0,255)

        _, contours, hierarchy = cv2.findContours(img3.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if hierarchy is not None:
            hierarchy=hierarchy[0]
        for c in range(len(contours)):
            #cv2.drawContours(gray2, contours[c], -1, 0, 2)
            M = cv2.moments(contours[c])
            cX = int(M['m10'] / (M['m00'] + 0.00001))
            cY = int(M['m01'] / (M['m00'] + 0.00001))
            epsilon = 0.1*cv2.arcLength(contours[c], True)
            approx = cv2.approxPolyDP(contours[c], epsilon, True)
            if (cv2.contourArea(contours[c])>100):
             #if(len(approx)>2&len(approx)<6):
             if (cY<310):
              #if hierarchy[c][2]<0:
                if cv2.contourArea(contours[c])<((gray.shape[0]*gray.shape[1])-0):
                    #cv2.drawContours(gray, contours[c], -1, 127, 2)
                    cv2.drawContours(gray2, contours[c], -1, 0, 2)
                    #cv2.circle(gray, (cX, cY), 7, 127, -1)
                    cv2.circle(gray2, (cX, cY), 7, 127, -1)


            #gray= random_noise(gray, mode='s&p',amount=0.3)

            #gray = np.array(255*gray, dtype = 'uint8')
            #gauss = np.random.normal(0,1,gray.size)
            #gauss = gauss.reshape(gray.shape[0],gray.shape[1]).astype('uint8')
            #noise = gray + gray * gauss


            shw=np.concatenate((img3,gray2),axis=1)
            gray=gray.astype('uint8')
            #clr=cv2.applyColorMap(gray, cv2.COLORMAP_H)
            #clr = cv2.GaussianBlur(clr, (49,49),0)
            #cv2.imshow("depth",clr)
            cv2.imshow("out",shw)
            cv2.waitKey(10)
            # cv2.imshow("cnts",gray)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

        #cv2.imshow('video', img3)

if __name__=='__main__':
    rospy.init_node('drone')
    drone = Drone()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()
