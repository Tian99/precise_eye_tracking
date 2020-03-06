#!/usr/bin/env python3

import cv2
import sys
import random
import pickle
import pic_analyze
from eye_canny import canny
from eye_circle import circle
from csv_analysis import read
from plot_data import plotting
from threshold import threshold
from pre_determination import determine 
from glint_detection import circle_glint

#The video frame is mostly 60 fps
class PupilTracking():

    def __init__(self, video, timing_fname="", num_tests=5, fps=60, show=False):
        """
        Three phases: 
        1. determination the best way to transfrom an image into computer readable, 
        2. track the pupil and glint movement as precise as possible
        3. Use the data provided and the data read, construct amn algorithm to precisely track the slight movement of vector between pupil and glint
        
        Starting with the first step
        pick five instances of image from the colleciton of images framed from the video
         Opens the Video file
        Video will be read from the command line
        Number of image traisl you want
        """
        super().__init__()
        self.fps = fps
        self.show = show
        self.num_tests = num_tests
        if timing_fname == "":
            timing_fname = 'input/testing_set/testing_1/10997_20180818_mri_1_view.csv'
            print("Warning: using default timing %s" % timing_fname)
        

        # convert video to series of frames
        self.number_frame = self.to_frame(video)
        print('To frame successful')

        # get random frames to test on
        self.random_num = self.rand(self.number_frame, self.num_tests)
        try:
            self.V, self.L, self.H, self.name_pic = self.pre_test(self.random_num, self.num_tests)
        except:
            print('Resizing factors too big to be useful')
            exit()

        #list of list that contains the whole set of testing data
        sets = self.file_data(timing_fname)
        print(sets)
        # [[6.0, 8.0, 10.0, 16.0], [20.0, 22.0, 24.0, 30.0], [40.0, 42.0, 44.0, 50.0], ....

        #Now print the results out and take a look
        print(self.V, self.L, self.H, self.name_pic)

        #Now do the analysis set by set// Starting to code the main part of the program        
        print('pretesting finished, starting analying the collection pictures using the paramaters')

        output_sets = self.frame_retrieve(sets, self.L, self.H)
        #Now the output_sets is obtained, next setp isd to analyze it.
        print('Data gethering complete')
        print('Starting to plot the data')
        plotting(output_sets)

    def frame_retrieve(self, sets, L, H):
        output_sets = []
        #Only need to get the frame around the critical area
        #60 frame/second
        ########################################################################
        #Change it to for loop later
        ########################################################################
        # for i in sets:
        i = sets[0]
        t_cue = i[0]
        t_vgs = i[1]
        t_dly = i[2]
        t_mgs = i[3]

        #Now, after the cue, the pupil should be staring at the center 
        show_center = range(self.fps*int(t_cue), self.fps*int(t_vgs))
        #After vgs, the eye should be staring at the picture
        show_loc = range(self.fps*int(t_vgs), self.fps*int(t_dly))
        #After dly, it should be staring at the center
        hide_center = range(self.fps*int(t_dly), self.fps*int(t_mgs))
        #After t_mgs, it should be staring at wherever it remembered
        #Turns out it always gonna be 2s --> for now
        hide_pic = range(self.fps*int(t_mgs), self.fps*(int(t_mgs) + 2))

        collections = [show_center, show_loc, hide_center, hide_pic]

        #Read the critical frame from the folder
        output_sets.append(self.critical_frame(collections, L, H))

        return output_sets

    #Append every frame data to the dictionary and return it back in a big listy
    def critical_frame(self, collections, L, H):
        count = 0
        dic = {}
        dic['s_center'] = []
        dic['s_loc'] = []
        dic['h_center'] = []
        dic['h_loc'] = []

        ncol = len(collections)
        for i in range(0, ncol):
            for file in collections[i]:
                case_name = 'analysis_set/kang%05d.png'%file
                image = cv2.imread(case_name)
                outcome = threshold(image, L, H)
                max_cor, max_collec, circled_cases= circle(count, outcome)
                if i == 0:
                    dic['s_center'].append(max_cor)
                elif i == 1:
                    dic['s_loc'].append(max_cor)
                elif i == 2:
                    dic['h_center'].append(max_cor)
                elif i == 3:
                    dic['h_loc'].append(max_cor)
                else:
                    print('Something went wrong')
                    exit()

                count += 1
            count = 0
            print('{}/{} section done'.format(i+1, ncol))
            print('\n\n')
        return dic


        
        # self.video_analyze(self.L, self.H)
    def file_data(self, timing_fname):
        current = []
        cue, vgs, dly, mgs = read(timing_fname)
        for i in range(0, len(cue)):
            current.append([cue[i], vgs[i], dly[i], mgs[i]])
        #Now start to narrow down the analysis rang
        #now the video file is 60 fps, and every video file is named according to the sequence
        return current


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
        #[(circle_1+circle_2), lower, uppert, 'frame_testing/kang%05d.png'%count]
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
        print('Starting to convert video to frames')
        cap = cv2.VideoCapture(video)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            #Write out individual frames just to test
            #Downscale the frame
            height = frame.shape[0]
            width = frame.shape[1]
            #Need to conserve one for the later analysis
            keep = frame
            #The first resize is for the real_analysis
            keep = cv2.resize(keep,(int(height), int(width)))
            #the second resize if for the analysis when determining parameters
            frame = cv2.resize(frame,(int(height/8), int(width/8)))
            cv2.imwrite('analysis_set/kang%05d.png'%i,keep)
            cv2.imwrite('frame_testing/kang%05d.png'%i,frame)
            #Then throw the image to threshold to process
            i+=1
        #Total number of frames
        return i


if __name__ == '__main__':

    # usage if wrong number of input args
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("USAGE: %s video.mov [timing.csv]" % sys.argv[0])
        exit()

    # pass all cli arguments (video, maybe timing) into class
    ######################################################################
    #TODO: change num_tests to 20 later
    ######################################################################
    PupilTracking(*sys.argv[1:], show=True, num_tests=5)


