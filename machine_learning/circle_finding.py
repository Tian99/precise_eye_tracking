import cv2
import numpy as np

def circle_finding():
    img = cv2.imread('testing.png', 0)
    print(img)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1 = 30, param2 = 20, minRadius = 0, maxRadius = 0)
    print(circles)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        print(i)
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    cv2.imwrite('detected circles',cimg)

circle_finding()