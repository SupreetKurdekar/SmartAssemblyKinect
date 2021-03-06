import cv2
from scipy import stats
import numpy as np
# function to display the coordinates of 
# of the points clicked on the image  
def click_event(event, x, y, flags, params): 
  
    # checking for left mouse clicks 
    if event == cv2.EVENT_LBUTTONDOWN: 
  
        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y) 
  
        # # displaying the coordinates 
        # # on the image window 
        # font = cv2.FONT_HERSHEY_SIMPLEX 
        # cv2.putText(img, str(x) + ',' +
        #             str(y), (x,y), font, 
        #             1, (255, 0, 0), 2) 
        # cv2.imshow('image', img) 
  
    # checking for right mouse clicks      
    if event==cv2.EVENT_RBUTTONDOWN: 
  
        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y) 
  
        # # displaying the coordinates 
        # # on the image window 
        # font = cv2.FONT_HERSHEY_SIMPLEX 
        # b = img[y, x, 0] 
        # g = img[y, x, 1] 
        # r = img[y, x, 2] 
        # cv2.putText(img, str(b) + ',' +
        #             str(g) + ',' + str(r), 
        #             (x,y), font, 1, 
        #             (255, 255, 0), 2) 
        # cv2.imshow('image', img) 

def normCrossCorrelation(img1,img2):
    # this function calculates the normalised cross correlation
    # for each channel
    # and returns the average across all channels for 
    # two crops of the same size

    if img1[0].shape == img2[0].shape:

        img1 = img1.reshape(-1, img1.shape[-1])
        img2 = img2.reshape(-1, img2.shape[-1])

        img1 = stats.zscore(img1, axis=0, ddof=1)
        img2 = stats.zscore(img2, axis=0, ddof=1)

        corr_per_channel = np.sum(img1*img2,axis=0)
        corr_per_channel = corr_per_channel/len(img1)
        avg_corr = np.mean(corr_per_channel)

        return avg_corr,corr_per_channel
    
    else:
        return None,None


def getContourMask(crop):

    # this function takes an image
    # returns the mask of the lasrgest contour of the 
    # image
    crop = cv2.GaussianBlur(crop,(5,5),0)
    imgray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours,heirarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # find the biggest countour (c) by the area
    MaxAreaContour = max(contours, key = cv2.contourArea)
    blank = np.zeros_like(crop)
    cv2.drawContours(blank, [MaxAreaContour], 0, (0,255,0), 3)
    outline = blank.copy()
    blank = cv2.cvtColor(blank,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(blank,127,255,cv2.THRESH_BINARY_INV)
    mask = np.broadcast_to(mask,(3,)+mask.shape)
    mask = mask.transpose(1,2,0)

    return mask

def gamma_correction(image,gamma):

    image = image.astype("float")
    image = (np.divide(image,255)**(1/gamma))*255
    return image.astype(np.uint8)

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

# Utils for ORB Feature matching

""" Clear matches for which NN ratio is > than threshold """
def filter_distance(matches):
    dist = [m.distance for m in matches]
    thres_dist = (sum(dist) / len(dist)) * ratio

    sel_matches = [m for m in matches if m.distance < thres_dist]
    #print '#selected matches:%d (out of %d)' % (len(sel_matches), len(matches))
    return sel_matches

""" keep only symmetric matches """
def filter_asymmetric(matches, matches2, k_scene, k_ftr):
    sel_matches = []
    for match1 in matches:
        for match2 in matches2:
            if match1.queryIdx < len(k_ftr) and match2.queryIdx < len(k_scene) and \
                match2.trainIdx < len(k_ftr) and match1.trainIdx < len(k_scene) and \
                            k_ftr[match1.queryIdx] == k_ftr[match2.trainIdx] and \
                            k_scene[match1.trainIdx] == k_scene[match2.queryIdx]:
                sel_matches.append(match1)
                break
    return sel_matches

def filter_ransac(matches, kp_scene, kp_ftr, countIterations=2):
    if countIterations < 1 or len(kp_scene) < minimalCountForHomography:
        return matches

    p_scene = []
    p_ftr = []
    for m in matches:
        p_scene.append(kp_scene[m.queryIdx].pt)
        p_ftr.append(kp_ftr[m.trainIdx].pt)

    if len(p_scene) < minimalCountForHomography:
        return None

    F, mask = cv2.findFundamentalMat(np.float32(p_ftr), np.float32(p_scene), cv2.FM_RANSAC)
    sel_matches = []
    for m, status in zip(matches, mask):
        if status:
            sel_matches.append(m)

    #print '#ransac selected matches:%d (out of %d)' % (len(sel_matches), len(matches))

    return filter_ransac(sel_matches, kp_scene, kp_ftr, countIterations-1)



def filter_matches(matches, matches2, k_scene, k_ftr):
    matches = filter_distance(matches)
    matches2 = filter_distance(matches2)
    matchesSym = filter_asymmetric(matches, matches2, k_scene, k_ftr)
    if len(k_scene) >= minimalCountForHomography:
        return filter_ransac(matchesSym, k_scene, k_ftr)