## This script uses skimage ssim structural similarity metric to check similarity between two images

import cv2
import skimage
import time
from skimage.metrics import structural_similarity as ssim

base_image_path = "C:\\Users\\Supreet\\VisionSystem\\CapturedImages\\2.png" 
test_image_path = "C:\\Users\\Supreet\\VisionSystem\\CapturedImages\\3.png"

base_img = cv2.imread(base_image_path)
test_img = cv2.imread(test_image_path)

img1 = base_img
img2 = test_img

# cv2.imshow("Image 1",img1)
# cv2.imshow("Image 2",img2)
# cv2.waitKey(0)

start = time.perf_counter()
score = ssim(img1,img2,multichannel=True)
end = time.perf_counter()
print(score)
print(end-start)