import cv2
import sys
import random
import pickle
import pic_analyze
from eye_canny import canny
from eye_circle import circle
from csv_analysis import read
from threshold import threshold
from pre_determination import determine 
from glint_detection import circle_glint

#The video frame is mostly 60 fps
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
        self.fps = 60
        video = self.user_input()
        filename = 'input/testing_set/testing_1/10997_20180818_mri_1_view.csv'
        self.num_tests = 1
        self.number_frame = self.to_frame(video)
        self.random_num = self.rand(self.number_frame, self.num_tests)
        try:
        	self.V, self.L, self.H, self.name_pic = self.pre_test(self.random_num, self.num_tests)
        except:
        	print('Resizing factors too big to be useful')
        	exit()
        #list of list that contains the whole set of testing data
        sets = self.file_data(filename)
        print(sets)
        #Now print the results out and take a look
        print(self.V, self.L, self.H, self.name_pic)
        #Now do the analysis set by set// Starting to code the main part of the program        
        print('pretesting finished, starting analying the collection pictures using the paramaters')

        self.frame_retrieve(sets)
    
    def frame_retrieve(self.sets):
    	#Only need to get the frame around the critical area
    	#60 frame/second
    	for i in sets:
    		t_cue = i[0]
    		t_vgs = i[1]
    		t_dly = i[2]
    		t_mgs = i[3]

	    	#Now, after the cue, the pupil should be staring at the center 
	    	show_center = range(fps*t_cue, fps*t_vgs)
	    	#After vgs, the eye should be staring at the picture
	    	show_loc = range(fps*t_vgs, fps*t_dly)
	    	#After dly, it should be staring at the center
	    	hide_center = range(fps*t_dly, fps*t_mgs)
	    	#After t_mgs, it should be staring at wherever it remembered
	    	#Turns out it always gonna be 2s --> for now
	    	hide_pic = range(fps*t_mgs, fps*(t_mgs + 2))

	    	#Read the critical frame from the folder
	    	for t in range(show_center):
	    		








        
        # self.video_analyze(self.L, self.H)
    def file_data(self, filename):
    	current = []
    	cue, vgs, dly, mgs = read(filename)
    	for i in range(0, len(cue)):
    		current.append([cue[i], vgs[i], dly[i], mgs[i]])
    	#Now start to narrow down the analysis rang
    	#now the video file is 60 fps, and every video file is named according to the sequence
    	return current

    def video_analyze(self, L, H):
    	#Self.L and seklf.H represent the lower and higher bound of the threshold
        outcome = threshold(image, self.L, self.H)
        #Now onyly need to analyze those before and after the cuing time + ro - 5s i suppose
        max_cor, max_collec = circle(count, outcome)
        #Video analyze finished
        print('Video analyze finished')

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
            frame = cv2.resize(frame,(int(height/9), int(width/9)))
            cv2.imwrite('analysis_set/kang%05d.png'%i,keep)
            cv2.imwrite('frame_testing/kang%05d.png'%i,frame)
            #Then throw the image to threshold to process
            i+=1
        #Total number of frames
        return i

if __name__ == '__main__':
    PupilTracking()


