import pandas as pd

def read(filename):
	data = pd.read_excel(filename)
	data.to_pickle('input/testing_set/testing_1/data.pkl')
	print('Finish converting')

read('input/testing_set/testing_1/file_1.xlsx')
