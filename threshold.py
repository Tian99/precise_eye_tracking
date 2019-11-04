
from PIL import Image
from eye_blur import blur
from blur_frame import blur_frame
from eye_canny import canny
import cv2

def threshold(image):
    #Blur it first
    imageObject = blur(image)
    
    shape_1 = image.shape[0]
    shape_2 = image.shape[1]
    #Cut it 
    cropped = imageObject[int((280/1776)*shape_1):shape_1, int((380/2364)*shape_2):int((2100/2364)*shape_2)] 

    _, threshold = cv2.threshold(cropped, 90, 255, cv2.THRESH_BINARY) 
    
    threshold = canny(threshold)
    


    # threshold = blur_frame(threshold)
    # cv2.imwrite('output/cropped.png', cropped)

    return threshold

# image = cv2.imread('input/sample.png')
# threshold(image)