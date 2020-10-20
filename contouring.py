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

fullImage = cv2.imread("C:\\Users\\Supreet\\VisionSystem\\twoStepBaseImages\\1.png")
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

state = 1

stateDictPath = os.path.join(basePath,baseStateDicts[state])
with open(stateDictPath) as json_file:
    state_data = json.load(json_file)

fullImage = np.array(state_data["Full Image"])
fullImage = fullImage.astype(np.uint8)
crop = np.array(state_data["Cropped Image"])
crop = crop.astype(np.uint8)
clone = crop.copy()
croppingRange = np.array(state_data["Pixels"])

236, 50, 26
ORANGE_MIN = np.array([215, 240, 125],np.uint8)
ORANGE_MAX = np.array([255, 255, 140],np.uint8)

hsv_img = cv2.cvtColor(crop,cv2.COLOR_BGR2HSV)

frame_threshed = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
cv2.imshow('output2.jpg', frame_threshed)
cv2.waitKey(0)


crop = cv2.GaussianBlur(crop,(5,5),0)
imgray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
thresh = cv2.Canny(imgray,0,100)
# Optimal threshold value is determined automatically.
# otsu_threshold, thresh = cv2.threshold(
#     imgray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,
# )
# ret, thresh = cv2.threshold(imgray, 0, 255, 0)
contours,heirarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# find the biggest countour (c) by the area
MaxAreaContour = max(contours, key = cv2.contourArea)
blank = np.zeros_like(crop)
cv2.drawContours(crop, contours, -1, (0,255,0), 3)

cv2.drawContours(blank, [MaxAreaContour], 0, (0,255,0), 3)
outline = blank.copy()
blank = cv2.cvtColor(blank,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(blank,127,255,cv2.THRESH_BINARY_INV)
mask = np.broadcast_to(mask,(3,)+mask.shape)
mask = mask.transpose(1,2,0)
print(mask.shape)
fullImage[croppingRange[0][1]:croppingRange[1][1], croppingRange[0][0]:croppingRange[1][0]] = cv2.bitwise_and(fullImage[croppingRange[0][1]:croppingRange[1][1], croppingRange[0][0]:croppingRange[1][0]],mask)
# fullImage[croppingRange[0][1]:croppingRange[1][1], croppingRange[0][0]:croppingRange[1][0]] += np.broadcast_to(outline,(3,)+outline.shape)

# cv2.imshow("Contours",mask)
cv2.imshow("Full",fullImage)
cv2.imshow("Crop",crop)

cv2.waitKey(0)

# for cnt in contours:
#     cv2.drawContours(crop, [cnt], 0, (0,255,0), 3)
#     temp = cv2.resize(crop,(400,400))
#     cv2.imshow("Contours",temp)

#     cv2.waitKey(0)
#     crop = clone
