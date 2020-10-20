################################################################################
### Sample program to stream 
### color data using opencv
### compare current color frame to knoen base frame
### output yes if above a threshold
################################################################################
import cv2
import numpy as np
import utils_PyKinectV2 as utils
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime


import skimage
from skimage.metrics import structural_similarity as ssim

import os
## Base image for state comparison
baseFolder = "C:\\Users\\Supreet\\VisionSystem\\BaseImagesForSSIM"
baseImageName = "FV_of_drill_mid_of_left_half_of_table.png"
baseImage = cv2.imread(os.path.join(baseFolder,baseImageName))

#############################
### Kinect runtime object ###
#############################
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)

depth_width, depth_height = kinect.depth_frame_desc.Width, kinect.depth_frame_desc.Height # Default: 512, 424
color_width, color_height = kinect.color_frame_desc.Width, kinect.color_frame_desc.Height # Default: 1920, 1080

id = 0
ssimProcessingTime = []
while True:
    ##############################
    ### Get images from camera ###
    ##############################
    if kinect.has_new_color_frame():

        color_frame      = kinect.get_last_color_frame() 
        # reshapr from 1d frame to 2d image
        color_img        = color_frame.reshape(((color_height, color_width, 4))).astype(np.uint8)
        # dropping alpha layer of photo
        color_img = color_img[:,:,0:-1]
        color_img = cv2.resize(color_img, (0,0), fx=0.5, fy=0.5) # Resize (1080, 1920, 4) into half (540, 960, 4)
        color_img = cv2.flip(color_img,1)

        cv2.imshow("Camera Feed",color_img)
        cv2.imshow("Base Image",baseImage)

        # score = ssim(baseImage,color_img,multichannel=True)
        # print(score)
        # id += 1
    
    key = cv2.waitKey(1)
    if key==27: # Press esc to break the loop
        break

kinect.close()
cv2.destroyAllWindows()