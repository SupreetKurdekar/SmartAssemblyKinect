import cv2
import numpy as np

MIN_MATCH_COUNT=30

detector=cv2.ORB_create(nfeatures=6000)

# # this is for flann and knn based matching
# FLANN_INDEX_KDITREE=0
# flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
# flann=cv2.FlannBasedMatcher(flannParam,{})

# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# cv2.BFMatcher.match()
# trainImg=cv2.imread("C:\\Users\\Supreet\\VisionSystem\\ObjDetData\\DrillCropped.png",0)
trainImg=cv2.imread("C:\\Users\\Supreet\\VisionSystem\\completeAssemblyTopViewFullImages\\Battery.png",0)

trainKP,trainDesc=detector.detectAndCompute(trainImg,None)
# trainDesc = np.float32(trainDesc)

################################################################################
### Sample program to stream 
### color data using opencv
################################################################################
import cv2
import numpy as np
import time

import utils_PyKinectV2 as utils
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import os

from visionUtils import click_event
import visionUtils

#########################
imagePath = "C:\\Users\\Supreet\\VisionSystem\\completeAssemblyTopViewFullImages"
img_counter = 0
#############################
### Kinect runtime object ###
#############################
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)

depth_width, depth_height = kinect.depth_frame_desc.Width, kinect.depth_frame_desc.Height # Default: 512, 424
color_width, color_height = kinect.color_frame_desc.Width, kinect.color_frame_desc.Height # Default: 1920, 1080

gamma = 0.5
invGamma = 1.0 / gamma
table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

while True:
    ##############################
    ### Get images from camera ###
    ##############################
    if kinect.has_new_color_frame():

        color_frame      = kinect.get_last_color_frame()
        
        #########################################
        ### Reshape from 1D frame to 2D image ###
        #########################################
        color_img        = color_frame.reshape(((color_height, color_width, 4))).astype(np.uint8)

        ######################################
        ### Display 2D images using OpenCV ###
        ######################################
        color_img_resize = cv2.resize(color_img, (0,0), fx=1, fy=1) # Resize (1080, 1920, 4) into half (540, 960, 4)
        color_img_resize = cv2.resize(color_img, (0,0), fx=1, fy=1) # Resize (1080, 1920, 4) into half (540, 960, 4)
        color_img_resize = cv2.flip(color_img_resize,0)

        color_img_resize = cv2.LUT(color_img_resize, table)

    # while True:
    #     ret, QueryImgBGR=cam.read()
        QueryImg=cv2.cvtColor(color_img_resize,cv2.COLOR_BGR2GRAY)
        queryKP,queryDesc=detector.detectAndCompute(QueryImg,None)
        # queryDesc = np.float32(queryDesc)
        # matches=flann.knnMatch(queryDesc,trainDesc,k=2)
        
        # Match descriptors.
        matches = bf.match(queryDesc,trainDesc)
        # bf.match()
        # # Sort them in the order of their distance.
        # matches = sorted(matches, key = lambda x:x.distance)
        print(len(trainKP))
        # Draw first 10 matches.
        # img3 = cv2.drawMatches(trainImg,trainKP,QueryImg,queryKP,matches,None, flags=2)

        tp = []
        qp = []
        for i,m in enumerate(matches):
            # print(i)
            # try:
            #     tp.append(trainKP[m.trainIdx].pt)
            #     qp.append(queryKP[m.queryIdx].pt)
            # except:
            #     pass

            # try:

            tp.append(trainKP[m.trainIdx].pt)
            qp.append(queryKP[m.queryIdx].pt)
            # except:
            #     pass

        tp,qp = np.float32((tp,qp))
        H,status = cv2.findHomography(tp,qp,cv2.RANSAC,1.0)
        h,w = trainImg.shape
        trainBorder = np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
        queryBorder = cv2.perspectiveTransform(trainBorder,H)
        cv2.polylines(color_img_resize,[np.int32(queryBorder)],True,(0,255,0),5)

        cv2.imshow("res",color_img_resize)
        # cv2.imshow("final",img3)
        if cv2.waitKey(1)==ord('q'):
            break


kinect.close()
cv2.destroyAllWindows()