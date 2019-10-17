import cv2
image = cv2.imread('input/Eye_tracking.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('output/testing.png',gray_image)
# bat.jpg is the batman image. 
img = cv2.imread('output/testing.png')  
# make sure that you have saved it in the same folder 
# You can change the kernel size as you want 
blurImg = cv2.blur(img,(3,3))  
cv2.imwrite('output/testing.png',blurImg) 
  
cv2.waitKey(0) 
cv2.destroyAllWindows() 
