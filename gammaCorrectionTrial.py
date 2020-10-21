import cv2
import numpy as np
import matplotlib as plt

image = cv2.imread("C:\\Users\\Supreet\\VisionSystem\\completeAssemblyTopViewFullImages\\0.png").astype("float")
image = cv2.resize(image,(600,424))

gamma = 2.5
print(gamma)

# print(np.max(image))
# print(np.min(image))

# image = image/255

# print(np.max(image))
# print(np.min(image))

# image = image ** gamma

# print(np.max(image))
# print(np.min(image))

# corr_image = image*255
corr_image = ((image/255)**gamma)*255
corr_image = corr_image.astype(np.uint8)
image = image.astype(np.uint8)

cv2.putText(corr_image, "g={}".format(gamma), (10, 30),
		cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)


cv2.imshow("Original Image",image)
cv2.imshow("Adjusted Image",corr_image)

cv2.waitKey(0)

