import cv2
import sys
import random
from pre_determination import determine 
from eye_blur import blur
from eye_canny import canny
from enhancement import enhance
from threshold import threshold
from eye_circle import circle
from glint_detection import circle_glint
import pickle



def main():
    #Three phases: 
    #1. determination the best way to transfrom an image into computer readable, 
    #2. track the pupil and glint movement as precise as possible
    #3. Use the data provided and the data read, construct amn algorithm to precisely track the slight movement of vector between pupil and glint
    
    #Starting with the first step
    #pick five instances of image from the colleciton of images framed from the video
    # Opens the Video file
    #Video will be read from the command line
    #Number of image traisl you want
    k = 20
    try:
        video = sys.argv[1]
    except IndexError:
    	print('Please type in the video file')

    number_frame = to_frame(video)
    #for now, everything will be processed after calling to_frame, later switch to multi_threading
    #Randomly pick 10 instances from the frame_testing
    random = rand(number_frame, k)
    #Got the best threshold value
    #Find the name in testing result which gives you the best
    V, L, H, name = pre_test(random, k)

    print(V, L, H, name)

    #Once successfully find the best
    

#///////////////////////////////////////////////
#Function methods
#?/////////////////////////////////////////////

def pre_test(random, k):
    grand_test = []
    for case in random:
        case_name = 'frame_testing/kang%05d.png'%case
        #Read in the image
        image = cv2.imread('input/testing_set/test0.png')
        result = determine(image, k)

        grand_test.append(result)
        
        #For the sake of keeping track of process
        k = k - 1

    grand_test.sort()
    
    #Best of the best should be
    result = grand_test[len(grand_test) - 1]

    V, L, H, name = result

    return V, L, H, name

def rand(number_frame, k):
    rand = []
    for i in range(k):
        r=random.randint(0, number_frame)
        if r not in rand: rand.append(r)
    return rand


def to_frame(video):
    #Video name tracker i
    i = 0
    cap= cv2.VideoCapture(video)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        #Write out individual frames just to test
        cv2.imwrite('frame_testing/kang%05d.png'%i,frame)
        #Then throw the image to threshold to process
        i+=1
    #Total number of frames
    return i

if __name__ == '__main__':
    main()


