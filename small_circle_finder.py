import cv2

def small(img):

    height = img.shape[0]
    width = img.shape[1]
    # print(width, height)

    _, threshold = cv2.threshold(img, 90, 255, cv2.THRESH_BINARY) 

    # for i in range(0, height):
    #     for j in range(0, width):
    #         if img[i,j] < 10:
 #                img[i,j] = 255
 #            else:
 #                img[i,j] = 0
 #    return img

    return threshold

image = cv2.imread('output/testing.png', cv2.COLOR_BGR2GRAY)
image = small(image)

cv2.imwrite('a.png', image)