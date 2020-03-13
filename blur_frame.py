import cv2

def blur_frame(frame):
	image = frame
	blurImg = cv2.blur(image, (60,60))

	return blurImg
