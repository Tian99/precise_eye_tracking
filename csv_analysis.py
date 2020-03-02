import pandas as pd
from pandas import DataFrame as df

def read(filename):
	cue = []
	vgs = []
	dly = []
	mgs = []
	#Well, don't know what this is, white it down first
	iti = []
	#Could only be read as csv when all the crap on top of the file is deleted
	data = pd.read_csv(filename)
	for axis, row in data.iterrows():
		#Now the things we need: cue, vgs,dly, mgs, and iti
		cue.append(row['cue'])
		vgs.append(row['vgs'])
		dly.append(row['dly'])
		mgs.append(row['mgs'])
		#And maybe append iti later
	return cue, vgs, dly, mgs

read('input/testing_set/testing_1/10997_20180818_mri_1_view.csv')