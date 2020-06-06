
#########################################
#the image generated with radius set to two will just be messed up, Hence, I let it to find radius itself
#######################################
import cv2
import sys
import math
import operator
import functools
import numpy as np
import multiprocessing
from collections import Counter
from numba import jit, cuda
from timeit import default_timer as timer

class circle_acc:
	def __init__(self, frame):
		#Only need one level of all three colors
	    # frame = np.array(frame[:,:,1])
	    self.Rmin = 20
	    self.Rmax = 50
	    self.height = frame.shape[0]
	    self.width = frame.shape[1]
	    [self.x, self.y] = np.where(frame >= 225)
	    self.angle = [i for i in range(0, 360, 2)]
	    self.r = [i for i in range(self.Rmin, self.Rmax)]
	    self.accumulator = {}
	    self.vector = np.vectorize(self.formula)
	    self.vectorMid = np.vectorize(self.middle)
	    self.vectorEnd = np.vectorize(self.end)
	    self.vector(self.x, self.y)

	def output(self):
		k = Counter(self.accumulator)
		tops = k.most_common(2)
		max_collec = [tops[0][1]]+[tops[1][1]]
		max_cor = [tops[0][0]]+[tops[1][0]]

		return max_cor, max_collec

	def formula(self,x,y):
		self.vectorMid(self.r, x, y)

	def middle(self, r, x, y):
		self.vectorEnd(np.array(self.angle), np.array([r]*len(self.angle)), np.array([x]*len(self.angle)), np.array([y]*len(self.angle)))

	def end(self, angle, r, x, y):
		#Cast it to a new coordinates
		x0 = int(x-(r*math.cos(math.radians(angle))))
		y0 = int(y-(r*math.sin(math.radians(angle))))

		# Checking if the center is within the range of image
		if x0>0 and x0<self.width and y0>0 and y0<self.height:
		  if (x0,y0,r) in self.accumulator:
		    self.accumulator[(x0,y0,r)]=self.accumulator[(x0,y0,r)]+1
		  else:
			    self.accumulator[(x0,y0,r)]=0

# function optimized to run on gpu
def circle(frame, name_count = None):
  # start = timer()
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
      if edged_image.item(y, x) >= 255:

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

  # BUG? - why do this for each? only second is returned?
  # Good point
  for x, y, r in max_cor:
    circled_cases = cv2.circle(original_image, (x,y), r, (0,0,255))
    cv2.imwrite('circled/test.png', circled_cases)
  # print(timer() - start)
  return max_cor, max_collec, circled_cases

def GPU_boost(edged_image, height, width, Rmin, Rmax):
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
    return accumulator
