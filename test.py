
from eye_circle import circle
import cv2


image = cv2.imread("test.png", cv2.IMREAD_UNCHANGED)
# print(image)
circle(image)