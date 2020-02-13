import cv2
import pickle
from eye_blur import blur
from eye_canny import canny
from eye_circle import circle
from threshold import threshold
from glint_detection import circle_glint

def to_file(appDict, address):
    pickle_out = open(address,"wb")
    pickle.dump(appDict, pickle_out)

def to_dict(coordinate, maximum):
    dic = {}
    li = []
    for j in range(0, len(maximum)):
        if(maximum[0] == maximum[1]):
            maximum[1] = maximum[1] - 1

        dic[maximum[j]] = list(coordinate[j])
    li.append(dic)

    return li

def image_choice():
    #///////////////////////////////////////////////////////
    #Only read ceetain images by choice to reduce the runtime of it
    task = cv2.imread('frame_testing/kang%05d.png'%i, cv2.IMREAD_UNCHANGED)
    #Circle the pupil
    coordinate, maximum = circle(i, task)
    #Circle the glint
    coordinate_glint, maximum_glint = circle_glint(i, task)
    data_pupil = to_dict(coordinate, maximum)
    data_glint = to_dict(coordinate_glint, maximum_glint)
    

def to_file(data_pupil, data_glint):
    print('Starting writing to file')
    to_file(data_pupil, "data/dict.pickle")
    to_file(data_glint, "data/dict_glint.pickle")
    #Draw the circle after all is finished
