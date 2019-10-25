
from PIL import Image
from eye_blur import blur
import cv2

def threshold(image):
	#Blur it first
	imageObject = blur(image)

	#Cut it 
    cropped = imageObject.crop((350,230,1700,3000))

	_, threshold = cv2.threshold(cropped, 100, 255, cv2.THRESH_BINARY) 
	cv2.imwrite('output/threshold.png', threshold)