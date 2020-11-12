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
imagePath = "C:\\Users\\Supreet\\VisionSystem\\ObjDetData"
img_counter = 2
#############################
### Kinect runtime object ###
#############################
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)

depth_width, depth_height = kinect.depth_frame_desc.Width, kinect.depth_frame_desc.Height # Default: 512, 424
color_width, color_height = kinect.color_frame_desc.Width, kinect.color_frame_desc.Height # Default: 1920, 1080

gamma = 0.4
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
        # color_img_resize = visionUtils.gamma_correction(color_img_resize,gamma)

        # Use Flip code 0 to flip vertically 
        # color_img_resize = cv2.flip(color_img_resize, 1)
        # depth_colormap   = cv2.applyColorMap(cv2.convertScaleAbs(depth_img, alpha=255/1500), cv2.COLORMAP_JET) # Scale to display from 0 mm to 1500 mm
        # infrared_img     = cv2.convertScaleAbs(infrared_img, alpha=255/65535) # Scale from uint16 to uint8
        
        # cv2.imshow('body index', body_index_img)                    # (424, 512)
        cv2.imshow('color', color_img_resize)                       # (540, 960, 4)
        # cv2.imshow('align color with body joints', align_color_img) # (424, 512)
        # cv2.imshow('depth', depth_colormap)                         # (424, 512)
        # cv2.imshow('infrared', infrared_img)                        # (424, 512)
        
    key = cv2.waitKey(1)
    if key==27: # Press esc to break the loop
        break
    elif key%256 == 32:
        # SPACE pressed
        img_name = "{}.png".format(img_counter)
        path = os.path.join(imagePath,img_name)
        cv2.imwrite(path, color_img_resize)
        print("{} written!".format(img_name))
        img_counter += 1
    elif key%256 == ord("q"):
        cv2.setMouseCallback('color', click_event)
    # elif key%256 == ord("c"):
    #     print("cropped")
    #     crop = color_img_resize[croppingRange[1][0]:croppingRange[1][1],croppingRange[0][0]:croppingRange[0][1]]
    #     img_name = "{}.png".format(img_counter)
    #     os.path.join(imagePath,img_name)
    #     cv2.imwrite(img_name, crop)
    #     print("{} written!".format(img_name))
    #     img_counter += 1        



kinect.close()
cv2.destroyAllWindows()