import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('output/testing.png',0)
print(img)

# Initiate FAST object with default values
fast = cv2.FastFeatureDetector_create()
print(fast)

# find and draw the keypoints
kp = fast.detect(img, None)
img2 = cv2.drawKeypoints(img, kp, outImage=np.array([]), color=(255,0,0))

# # Print all default params
# print ("Threshold: ", fast.getInt('threshold'))
# print ("nonmaxSuppression: ", fast.getBool('nonmaxSuppression'))
# print ("neighborhood: ", fast.getInt('type'))
# print ("Total Keypoints with nonmaxSuppression: ", len(kp))

cv2.imwrite('output/fast_true.png',img2)

