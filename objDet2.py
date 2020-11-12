import numpy as np
import cv2
import matplotlib.pyplot as plt

img1 = cv2.imread('C:\\Users\\Supreet\\VisionSystem\\completeAssemblyTopViewFullImages\\Battery.png',0)
img2 = cv2.imread('C:\\Users\\Supreet\\VisionSystem\\ObjDetData\\2.png',0)
fullImage = cv2.imread('C:\\Users\\Supreet\\VisionSystem\\ObjDetData\\2.png')

topNpoints = 10

orb = cv2.ORB_create(nfeatures=8000,patchSize=30)

kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING2, crossCheck=True)

matches = bf.match(des2,des1)
matches2 = bf.match(des1,des2)
matches = sorted(matches, key = lambda x:x.distance)
matches2 = sorted(matches2, key = lambda x:x.distance)

img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches2[:topNpoints],None, flags=2)

tp = []
qp = []
for i,m in enumerate(matches[:topNpoints]):
    # print(i)
    # try:
    #     tp.append(trainKP[m.trainIdx].pt)
    #     qp.append(queryKP[m.queryIdx].pt)
    # except:
    #     pass

    # try:

    tp.append(kp1[m.trainIdx].pt)
    qp.append(kp2[m.queryIdx].pt)
    # except:
    #     pass

tp,qp = np.float32((tp,qp))
H,status = cv2.findHomography(tp,qp,cv2.RANSAC,1.0,maxIters=5000)
h,w = img1.shape
trainBorder = np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
queryBorder = cv2.perspectiveTransform(trainBorder,H)
cv2.polylines(fullImage,[np.int32(queryBorder)],True,(0,255,0),5)

cv2.imshow("res",fullImage)
cv2.imshow("keyPoints",img3)
# cv2.imshow("final",img3)
cv2.waitKey(0)