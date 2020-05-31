
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
@jit
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

  # BUG? - why do this for each? only second is returned?
  # Good point
  for x, y, r in max_cor:
    circled_cases = cv2.circle(original_image, (x,y), r, (0,0,255))
    cv2.imwrite('circled/test.png', circled_cases)
  # print(timer() - start)
  return max_cor, max_collec, circled_cases

# def ccast(yx, r, t, width, height):
#     """
#     at angle t and radius r
#     return if x,y is within range
#     >>> plt.imshow(ccast(yx,22,180,width,height))
#     """
#     #Cast it to a new coordinates
#     y0 = (yx[0] - (r * math.sin(t))).astype(int) 
#     x0 = (yx[1] - (r * math.cos(t))).astype(int) 
#     # Checking if the center is within the range of image
#     i = np.logical_and.reduce((y0 > 0, y0< height, x0>0, x0<width))
#     # create matrix with one if in range
#     v = np.zeros([height, width])
#     if(len(i) > 0):
#         v[y0[i],x0[i]] = 1
#     return v

# def sum_angles(yx, r, w, h, by=2):
#     """ sum the circles for over all angles """
#     angles = [math.radians(t) for t in range(0, 360, by)]
#     s = np.sum([ccast(yx, r, a, w, h) for a in angles], axis=0)
#     return(s)

# def plot_radlist(rs):
#     import matplotlib.pyplot as plt
#     ns = math.sqrt(len(rs))
#     fg, ax = plt.subplots(math.ceil(ns),math.ceil(ns))
#     for i, r in enumerate(rs):
#         x=math.floor(i/ns)
#         y=i%math.ceil(ns)
#         mi=np.unravel_index(np.argmax(r), r.shape)
#         mv=r[mi]
#         ax[x,y].imshow(r)
#         ax[x,y].set_title("r=%d; m=%d @ %s" % (radi[i], mv, mi))
#         ax[x,y].axis('off')
#         ax[x,y].annotate("%d" % mv, xy=mi, color='white')


# def circle_vectorized(frame, N=2, show=False):
#     """
#     use vectorized matricies to calc circle
#     >>> frame=threshold(cv2.imread('./analysis_set/kang00013.png'),100,8)
#     >>> # import matplotlib.pyplot as plt; plt.ion(); plt.imshow(frame);
#     """
#     (height, width) = frame.shape
#     (Rmin, Rmax) = (20, 50)
  
#     # find coords of edges
#     yx = np.where(frame >= 255)
#     # large list of r,t pairs for every r_min-r_max and degree (by 2)
#     # TODO: there is porbably math to show some of this space is redundant?
#     #   e.g. exclude x,y Rmin from image sides?
#     #   xy = xy[xy[:,0] > Rmin and xy[:,0] < width - Rmax, xy[0,:] > Rmin and xy[0,:] < height - Rmax]
#     #rng = [(r,math.radians(t)) for r in range(Rmin, Rmax, 2) for t in range(0, 360, 2)]
#     radi = range(Rmin,Rmax,2)
#     # for all the xy pairs on an edge,
#     #  make a cirlce matrix for each angle
#     #  and sum
#     rs = [sum_angles(yx, r, width, height) for r in radi]

#     # view it maybe
#     if show: plot_radlist(rs)
    
    
#     # # -- best only -- 
#     # (ri, yi, xi) = np.unravel_index(np.argmax(rs),shape)
#     # max_value = rs[ri][yi,xi]
#     # max_coordinate = (xi,yi,radi[ri])

#     # -- top N --
#     rs = np.array(rs)
#     i = np.argpartition(rs.flatten(), -N)[-N:]
#     vryx = [[rs[ii], radi[ii[0]], *ii[1:] ] for ii in
#              [np.unravel_index(ii, rs.shape) for ii in i]]
    
  
#     print('big_circle vryx')
#     print(vryx)

#     original_image = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

#     for (v, y, x, r) in vryx:
#       circled_cases = cv2.circle(original_image, (x,y), r, (0,0,255))
  
#     return(vryx)

#     return max_cor, max_collec, circled_cases
