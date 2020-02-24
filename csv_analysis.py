import pandas as pd
import dataframe as df

def read(filename):
	#Could only be read as csv when all the crap on top of the file is deleted
	data = pd.read_csv(filename)
	for axis, row in data.iterrows():
		#Now the things we need: cue, vgs,dly, mgs, and isi
		print(axis)

read('input/testing_set/testing_1/10997_20180818_mri_1_view.csv')