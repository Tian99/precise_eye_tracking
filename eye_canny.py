import cv2
import numpy as np


def canny(img):
	edges = cv2.Canny(img,30, 40) #200, 200 One line					cct
	return edges
