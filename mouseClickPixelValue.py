################################################################################
### Sample program to stream 
### color data using opencv
################################################################################
import cv2
import numpy as np
import utils_PyKinectV2 as utils
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime

from visionUtils import click_event

#############################
### Kinect runtime object ###
#############################
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)

depth_width, depth_height = kinect.depth_frame_desc.Width, kinect.depth_frame_desc.Height # Default: 512, 424
color_width, color_height = kinect.color_frame_desc.Width, kinect.color_frame_desc.Height # Default: 1920, 1080

while True:
    ##############################
    ### Get images from camera ###
    ##############################
    if kinect.has_new_color_frame():

        color_frame      = kinect.get_last_color_frame()

        
        #########################################
        ### Reshape from 1D frame to 2D image ###
        #########################################
        # body_index_img   = body_index_frame.reshape(((depth_height, depth_width))).astype(np.uint8) 
        color_img        = color_frame.reshape(((color_height, color_width, 4))).astype(np.uint8)
        # depth_img        = depth_frame.reshape(((depth_height, depth_width))).astype(np.uint16) 
        # infrared_img     = infrared_frame.reshape(((depth_height, depth_width))).astype(np.uint16)

        ###############################################
        ### Useful functions in utils_PyKinectV2.py ###
        ###############################################
        # align_color_img = utils.get_align_color_image(kinect, color_img)
        # align_color_img = utils.draw_bodyframe(body_frame, kinect, align_color_img) # Overlay body joints on align_color_img
        # body_index_img  = utils.color_body_index(kinect, body_index_img) # Add color to body_index_img

        ######################################
        ### Display 2D images using OpenCV ###
        ######################################
        color_img_resize = cv2.resize(color_img, (0,0), fx=0.5, fy=0.5) # Resize (1080, 1920, 4) into half (540, 960, 4)
        # depth_colormap   = cv2.applyColorMap(cv2.convertScaleAbs(depth_img, alpha=255/1500), cv2.COLORMAP_JET) # Scale to display from 0 mm to 1500 mm
        # infrared_img     = cv2.convertScaleAbs(infrared_img, alpha=255/65535) # Scale from uint16 to uint8
        
        # cv2.imshow('body index', body_index_img)                    # (424, 512)
        cv2.imshow('color', color_img_resize)                       # (540, 960, 4)
        # setting mouse hadler for the image 
        # and calling the click_event() function 
        cv2.setMouseCallback('color', click_event) 

    key = cv2.waitKey(2)
    if key==27: # Press esc to break the loop
        break

kinect.close()
cv2.destroyAllWindows()