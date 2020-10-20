################################################################################
### Sample program to stream 
### color data using opencv
### compare current color frame to knoen base frame
### output yes if above a threshold
### doing this throughout states
################################################################################
import cv2
import numpy as np
import json

import skimage
from skimage.metrics import structural_similarity as ssim

import utils_PyKinectV2 as utils
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime

import visionUtils as vUtils

import os

## test Setup
basePath = "C:\\Users\\Supreet\\VisionSystem\\croppedStates"
# get the names of the dictionaries
baseStateDicts = os.listdir(basePath)
thresholds = [95,95]
numStates = len(baseStateDicts)

#############################
### Kinect runtime object ###
#############################
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)

depth_width, depth_height = kinect.depth_frame_desc.Width, kinect.depth_frame_desc.Height # Default: 512, 424
color_width, color_height = kinect.color_frame_desc.Width, kinect.color_frame_desc.Height # Default: 1920, 1080

frame_array = []
fps = 10

for state,thresh in zip(range(0,numStates),thresholds):
    score = 0

    # load the dictionary

    # load the images as numpy arrays

    # get Cropping range


    stateDictPath = os.path.join(basePath,baseStateDicts[state])
    with open(stateDictPath) as json_file:
        state_data = json.load(json_file)

    fullImage = np.array(state_data["Full Image"]).astype(np.uint8)
    crop = np.array(state_data["Cropped Image"])
    crop = crop.astype(np.uint8)
    croppingRange = np.array(state_data["Pixels"])
    mask = vUtils.getContourMask(crop)

    while score < thresh:
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

            current_crop = color_img[croppingRange[0][1]:croppingRange[1][1], croppingRange[0][0]:croppingRange[1][0]]
            # print(crop.shape)
            score,_ = vUtils.normCrossCorrelation(crop,current_crop)
            color_img[croppingRange[0][1]:croppingRange[1][1], croppingRange[0][0]:croppingRange[1][0]] = cv2.bitwise_and(color_img[croppingRange[0][1]:croppingRange[1][1], croppingRange[0][0]:croppingRange[1][0]],mask)

            # Window name in which image is displayed 
            window_name = 'Camera'
            
            # font 
            font = cv2.FONT_HERSHEY_SIMPLEX 
            
            # org 
            org = (50, 50) 
            
            # fontScale 
            fontScale = 1
            
            # Blue color in BGR 
            color = (255, 0, 0) 
            
            # Line thickness of 2 px 
            thickness = 2
            
            # Using cv2.putText() method 
            color_img = cv2.putText(color_img, str(score), org, font,  
                            fontScale, color, thickness, cv2.LINE_AA) 

            size = (color_img.shape[0],color_img.shape[1])

            cv2.imshow("Camera",color_img)
            # cv2.imshow("Crop",crop)
            # cv2.imshow("current_crop",current_crop)

            #inserting the frames into an image array
            frame_array.append(color_img)
        
        key = cv2.waitKey(1)
        if key==27: # Press esc to break the loop
            break

    key = cv2.waitKey(1)
    if key==27: # Press esc to break the loop
        break

out = cv2.VideoWriter("vid6.avi",cv2.VideoWriter_fourcc(*'XVID'), fps, (540,960))
for i in range(len(frame_array)):
    # writing to a image array
    out.write(frame_array[i])
out.release()