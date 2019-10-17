import cv2
import numpy as np

img = cv2.imread('output/testing.png',0)
edges = cv2.Canny(img,45,45) #200, 200 One line
							 # 45, 45 Two lines

cv2.imwrite('output/eye_canny.png', edges)
