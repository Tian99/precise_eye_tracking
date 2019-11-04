import cv2
from eye_blur import blur
from eye_canny import canny
from enhancement import enhance
from threshold import threshold
from eye_circle import circle
from glint_detection import circle_glint
import pickle
 
def to_file(appDict):
    pickle_out = open("data/dict.pickle","wb")
    pickle.dump(appDict, pickle_out)
#Dictionary that have every data in it
dic = {}
li = []
# Opens the Video file
cap= cv2.VideoCapture('trim.mov')
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

    for j in range(0, len(maximum)):

        if(maximum[0] == maximum[1]):
            maximum[1] = maximum[1] - 1

        dic[maximum[j]] = list(coordinate[j])
    li.append(dic)
    to_file(li)
    
    #Renew the dictionary
    dic = {}
    i+=1
#Draw the circle after all is finished
 
cap.release()
cv2.destroyAllWindows()