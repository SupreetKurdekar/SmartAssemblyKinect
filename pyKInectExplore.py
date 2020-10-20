from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2

kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)
i = 0
while i < 10:
# --- Getting frames and drawing
# if kinect.has_new_color_frame():
    frame = kinect.get_last_color_frame()
    # print(frame.shape)
    # print(type(frame))
    frame = frame.astype(np.uint16)
    print(frame.shape)
    print(type(frame))
    # frame = np.reshape(frame, (424, 512))
    # img = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    # output = cv2.bilateralFilter(img, 9, 150, 75)
    # cv2.imshow('KINECT Video Stream', frame)
    frame = None
    i += 1

    key = cv2.waitKey(1)
    if key == 27: break