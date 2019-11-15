from threshold import threshold
from eye_circle import circle
import cv2


def determine(image):
	guessing = []
	count = 0
	#Get all the possible canny image throught all the threshold
	#The eyeball should always be the darkest pixel in the image, so the uppert would be set to 255 for now
	uppert = 255

	#Set lower t between 50 and 120 
	lowert = range(50,110)

	for i in lowert:
	    count = count + 1
	    #Canny image
	    outcome = threshold(image, i, uppert)
	    #Run the hough transform on each outcome
	    max_cor, max_collec = circle(count, outcome)
	    circle_1, circle_2 = max_collec
	    guessing.append([(circle_1+circle_2), 'frame_testing/kang%05d.png'%count])

	    print('--------------------------------')
	    print('progress:'+str(count/len(lowert)))
	    print('--------------------------------')

	guessing.sort()

	result = guessing[len(guessing)-1]

	return cv2.imread(result)

image = cv2.imread('input/testing_set/test0.png')

determine(image)


