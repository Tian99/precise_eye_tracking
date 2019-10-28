import cv2
import numpy as np


def canny(img):
	edges = cv2.Canny(img,20, 20) #200, 200 One line					cct
	return edges
