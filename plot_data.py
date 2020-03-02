#Now it's time to plot the data for a better insight

import matplotlib.pyplot as plt
import numpy as np

def plotting(dic):
	fig = plt.figure()
	ax1 = fig.add_subplot(111)

	print(dic)

	x_s_center = np.asarray(dic['s_center'])[:, 0]
	y_s_center = np.asarray(dic['s_center'])[:, 1]
	x_s_loc = np.asarray(dic['s_loc'])[:, 0]
	y_s_loc = np.asarray(dic['s_loc'])[:, 1]
	x_h_center = np.asarray(dic['h_center'])[:, 0]
	y_h_center = np.asarray(dic['h_center'])[:, 1]
	x_h_loc = np.asarray(dic['h_loc'])[:, 0]
	y_h_loc = np.asarray(dic['h_loc'])[:, 1]

	ax1.scatter(x_s_center, y_s_center, s=10, c='b', label='first')
	ax1.scatter(x_s_loc, y_s_loc, s=10, c='r', label='second')
	ax1.scatter(x_h_center, y_h_center, s=10, c='g', label='thrid')
	ax1.scatter(x_h_loc, y_h_loc, s=10, c='o', label='forth')

