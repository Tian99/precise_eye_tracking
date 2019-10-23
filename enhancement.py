# Load image
import cv2
import numpy as np
from matplotlib import pyplot as plt

def enhance(image):
	image_enhanced = cv2.equalizeHist(image, 100)

	return image_enhanced