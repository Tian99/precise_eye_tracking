import cv2
from eye_blur import blur
from eye_canny import canny
from enhancement import enhance
from threshold import threshold
from eye_circle import circle
from glint_detection import circle_glint
import pickle

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

# Opens the Video file
cap= cv2.VideoCapture('/Volumes/L/Data/Tasks/MGSEncMem/7T/11763_20190507/11763_20190506_run1_151744.avi.avi')
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    frame = threshold(frame)

    # frame = canny(frame)
    cv2.imwrite('frame/kang%05d.png'%i,frame)

    #Reread the image and draw the circle on it
    task = cv2.imread('frame/kang%05d.png'%i, cv2.IMREAD_UNCHANGED)
    coordinate, maximum = circle(i, task)
    print(i)
    print('--------------------------')
    coordinate_glint, maximum_glint = circle_glint(i, task)

    data_pupil = to_dict(coordinate, maximum)
    data_glint = to_dict(coordinate_glint, maximum_glint)


    to_file(data_pupil, "data/dict.pickle")
    to_file(data_glint, "data/dict_glint.pickle")

    #Renew the dictionary
    dic = {}
    i+=1
#Draw the circle after all is finished

cap.release()
cv2.destroyAllWindows()
