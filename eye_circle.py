
#########################################
#the image generated with radius set to two will just be messed up, Hence, I let it to find radius itself
########################################

import cv2,sys
import numpy as np
import operator
import math

def circle(name_count, frame):
  original_image = frame # Input file image
  edged_image = frame #Input image for the edged image
  height = edged_image.shape[0]
  width = edged_image.shape[1]


  Rmin = 20
  Rmax = 50

  # Initialise Accumulator as a Dictionary with x0, y0 and r as tuples and votes as values
  accumulator = {}

  # Loop over the image
  for y in range(0,height):
    for x in range(0,width):
      # If an edge pixel is found..
      if edged_image.item(y,x) >= 255:

        for r in range(Rmin,Rmax,2):
          for t in range(0,360,2):

            #Cast it to a new coordinates
            x0 = int(x-(r*math.cos(math.radians(t))))
            y0 = int(y-(r*math.sin(math.radians(t))))

            # Checking if the center is within the range of image
            if x0>0 and x0<width and y0>0 and y0<height:
              if (x0,y0,r) in accumulator:
                accumulator[(x0,y0,r)]=accumulator[(x0,y0,r)]+1
              else:
                accumulator[(x0,y0,r)]=0
  #print(accumulator
  #Iterate through the dictionary to find the max values
  max_cor = [] #Store the coordinates
  max_collec = [] #Store the max number
  max_coordinate = None
  max_value = 0
  count = 2 #First try 2

  #Somehow it is ranked from highest to lowest
  for i in range(count):
      for k, v in accumulator.items():
          if v > max_value:
            #Find the max votes in the accumulator
            max_value = v
            max_coordinate = k

      max_collec.append(max_value)
      #Zero out max
      max_value = 0
      #Append max position
      max_cor.append(max_coordinate)
      #Zero out that position
      accumulator[max_coordinate] = 0

  print('big_circle')
  #Show the x,y,and radius
  #If the x and y diverge too far away from each other, just cateforize it as the eye close
  print(max_cor)
  #Show the vote on each circle
  print(max_collec)

  original_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2RGB)

  for x, y, r in max_cor:
    circled_cases = cv2.circle(original_image, (x,y), r, (0,0,255))

  return max_cor, max_collec, circled_cases
