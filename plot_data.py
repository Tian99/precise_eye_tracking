#Now it's time to plot the data for a better insight

import matplotlib.pyplot as plt
import numpy as np

def plotting(dic):
	size = 0
	#Because it is a list that passed in, get the first one
	dic = data_format(dic)
	fig = plt.figure()
	ax1 = fig.add_subplot(111)

	print(dic)

	y_s_center = np.asarray(dic['s_center'])[:, 0]
	x_s_center = np.asarray(create_x(len(y_s_center), size))
	print(x_s_center.size)
	print(y_s_center.size)

	y_s_loc = np.asarray(dic['s_loc'])[:, 0]
	size += len(y_s_center)
	x_s_loc = np.asarray(create_x(len(y_s_loc), size))
	y_h_center = np.asarray(dic['h_center'])[:, 0]
	size += len(y_s_loc)
	x_h_center = np.asarray(create_x(len(y_h_center), size))
	y_h_loc = np.asarray(dic['h_loc'])[:, 0]
	size += len(y_h_center)
	x_h_loc = np.asarray(create_x(len(y_h_loc), size))

	ax1.scatter(x_s_center, y_s_center, marker = 'd', c='b', label='first')
	ax1.scatter(x_s_loc, y_s_loc, marker = 'o', c='r', label='second')
	ax1.scatter(x_h_center, y_h_center, marker = 'x', c='g', label='thrid')
	ax1.scatter(x_h_loc, y_h_loc, marker = 'v', c='y', label='forth')

	plt.show()

#Format the data first
def data_format(dic):
	new_dic = {}
	new_dic['s_center'] = []
	new_dic['s_loc'] = []
	new_dic['h_center'] = []
	new_dic['h_loc'] = []
	dic = dic[0]
	for i in dic:
		for j in dic[i]:
			if abs(j[0][0] - j[1][0]) < 30:
				new_dic[i].append(j[0])

	return new_dic

def create_x(length, size):
	li = []
	for i in range(0, length):
		li.append(i+size)
	return li



