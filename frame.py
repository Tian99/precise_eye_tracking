import cv2
from eye_blur import blur
from enhancement import enhance
from threshold import threshold
 
# Opens the Video file
cap= cv2.VideoCapture('trim.mov')
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    frame = threshold(frame)
    #Blur the frame
    cv2.imwrite('frame/kang%05d.png'%i,frame)
    i+=1
 
cap.release()
cv2.destroyAllWindows()