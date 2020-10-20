import cv2
import visionUtils

crop1 = cv2.imread("C:\\Users\\Supreet\\VisionSystem\\twoStepBaseImages\\cropped_1.png")
full1 = cv2.imread("C:\\Users\\Supreet\\VisionSystem\\twoStepBaseImages\\full_1.png")


croppingRange = [[245,360],[115,325]]

crop = full1[croppingRange[1][0]:croppingRange[1][1],croppingRange[0][0]:croppingRange[0][1]]

# print(crop.shape)
# cv2.imshow("old Crop",crop1)
# cv2.imshow("new crop",crop)

score = visionUtils.normCrossCorrelation(crop,crop)
print(score)

cv2.waitKey(0)