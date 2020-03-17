import cv2
from PIL import Image
from eye_blur import blur
from eye_canny import canny

def threshold(image, lowert, uppert):
    #Blur it first
    imageObject = blur(image)
    
    shape_1 = image.shape[0]
    shape_2 = image.shape[1]
    #Cut it
    #Don't crop, see how it goes
    #cropped = imageObject[int((280/1776)*shape_1):shape_1, int((380/2364)*shape_2):int((2100/2364)*shape_2)] 
    _, threshold = cv2.threshold(imageObject, lowert, uppert, cv2.THRESH_BINARY) 
    
    threshold = canny(threshold)

    return threshold
