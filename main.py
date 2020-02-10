import cv2
import sys
import random
import pickle
from eye_blur import blur
from eye_canny import canny
from eye_circle import circle
from enhancement import enhance
from threshold import threshold
from pre_determination import determine 
from glint_detection import circle_glint

class PupilTracking():

    def __init__(self):
        ''''''
        #Three phases: 
        #1. determination the best way to transfrom an image into computer readable, 
        #2. track the pupil and glint movement as precise as possible
        #3. Use the data provided and the data read, construct amn algorithm to precisely track the slight movement of vector between pupil and glint
        
        #Starting with the first step
        #pick five instances of image from the colleciton of images framed from the video
        # Opens the Video file
        #Video will be read from the command line
        #Number of image traisl you want
        ''''''
        super().__init__()
        video = self.user_input()
        self.num_tests = 20 
        self.number_frame = self.to_frame(video)
        self.random_num = self.rand(self.number_frame, self.num_tests)
        self.V, self.L, self.H, self.name_pic = self.pre_test(self.random_num, self.num_tests)

        #Now print the results out and take a look
        print(self.V, self.L, self.H, self.name_pic)

    #Once successfully find the best

    def user_input(self):
        try:
            video = sys.argv[1]
        except IndexError:
            print('Please type in the video file')
            exit()
        return video

    def pre_test(self, random, k):
        grand_test = []
        for case in random:
            #Read the file using the name constituted by the random number and naming conventions
            case_name = 'frame_testing/kang%05d.png'%case
            image = cv2.imread(case_name)

            #Find the best parameters for different threshold of one image of 20 images picked randomly
            result = determine(image, k)
            grand_test.append(result)
            #For the sake of keeping track of process
            k = k - 1
        grand_test.sort()
        #Best of the best should be
        result = grand_test[len(grand_test) - 1]
        #[(circle_1+circle_2), i, uppert, 'frame_testing/kang%05d.png'%count]
        V, L, H, name = result
        #Here returned the best parameters there is
        return V, L, H, name

    #To get 20 random frame to test out of all the frames
    def rand(self, number_frame, k):
        rand = []
        for i in range(k):
            r = random.randint(0, number_frame)
            if r not in rand: rand.append(r)
        return rand

    #Method to convert the whole video into frames
    def to_frame(self, video, i = 0):
        cap = cv2.VideoCapture(video)
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
    PupilTracking()


