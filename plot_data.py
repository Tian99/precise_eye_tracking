#Now it's time to plot the data for a better insight

import matplotlib.pyplot as plt
import numpy as np

def plotting(dic):
	#Because it is a list that passed in, get the first one
	# dic = dic[0] 
	fig = plt.figure()
	ax1 = fig.add_subplot(111)

	print(dic)

	x_s_center = np.asarray(dic['s_center'])[:, 0]
	y_s_center = np.asarray([1]*len(x_s_center))
	print(x_s_center.size)
	print(y_s_center.size)

	x_s_loc = np.asarray(dic['s_loc'])[:, 0]
	y_s_loc = np.asarray([1]*len(x_s_loc))
	x_h_center = np.asarray(dic['h_center'])[:, 0]
	y_h_center = np.asarray([1]*len(x_h_center))
	x_h_loc = np.asarray(dic['h_loc'])[:, 0]
	y_h_loc = np.asarray([1]*len(x_h_loc))

	ax1.scatter(x_s_center, y_s_center, marker = 'd', c='b', label='first')
	ax1.scatter(x_s_loc, y_s_loc, marker = 'o', c='r', label='second')
	ax1.scatter(x_h_center, y_h_center, marker = 'x', c='g', label='thrid')
	ax1.scatter(x_h_loc, y_h_loc, marker = 'v', c='y', label='forth')

	ax1.show()
