import cv2

def blur_frame(frame):
	image = frame
	blurImg = cv2.blur(image, (20,20))

	return blurImg
