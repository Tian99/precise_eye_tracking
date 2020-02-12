from threshold import threshold
from eye_circle import circle
import cv2


def determine(image, k):
    #Get all the possible canny image throught all the threshold
    #The eyeball should always be the darkest pixel in the image, so the uppert would be set to 255 for now
    guessing = []
    count = 0
    uppert = 255
    i = 0

    #Set lower t between 50 and 120 
    lowert = range(50,120)

    for low in lowert:
        count = count + 1
        #Canny image
        outcome = threshold(image, low, uppert)
        #Run the hough transform on each outcome
        #count is simply the naning convention
        max_cor, max_collec, circled_cases = circle(count, outcome)
        circle_1, circle_2 = max_collec
        #circle_1+circle_2 is the summation of two highest votes with coordinates
        guessing.append([(circle_1+circle_2), low, uppert, 'frame_testing/kang%05d.png'%count])

        print('--------------------------------')
        print('progress:'+str(count/len(lowert)))
        print('with %s more left'%str(k))
        print('--------------------------------')

    #Sort the best overall and get the best result and picture overall
    guessing.sort()
    result = guessing[len(guessing)-1]
    result_image = cv2.imread(result[3])
    cv2.imwrite('pretesting/%s.png'%i, circled_cases)
    #Write the image to the destinated folder to better examine
    cv2.imwrite('testing_result/%s.png'%i, result_image)
    i+=1
    return result


