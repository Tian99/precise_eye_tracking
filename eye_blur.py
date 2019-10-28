import cv2

def blur(frame):

	image = frame
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurImg = cv2.blur(gray_image,(10,10))  
	#cv2.imwrite('output/testing.png',blurImg) b
	return blurImg


