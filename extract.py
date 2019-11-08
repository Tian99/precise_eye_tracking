import calibration
import numpy as np
import matrix_extraction as extract

#Read the data file first and extract the event_str
result = extract.read_arrington('/Volumes/L/Data/Tasks/MGSEncMem/7T/11763_20190507/11763_20190506_run1_151744.txt')

#got all the useful file from the origional file
#Start to prepare for the calibration

def get_cues(result):
    str = result['event_str']
    #Return a list that contains each state in every frame
    return str

def construction(result):
    origin = None
    calibrated = None
    for i in range(0, len(result['x_gaze'])):
        x_oin = result['x_gaze'][i]
        y_oin = result['y_gaze'][i]

        x_cali = result['x_correctedgaze'][i]
        y_cali = result['y_correctedgaze'][i]

        if i < 1:
            origin = [[x_oin, y_oin]]
            calibrated = [[x_cali, y_cali]]
        else:
            cali_part = [[x_oin, y_oin]]
            origin_part = [[x_oin, y_oin]]
            origin = np.concatenate((origin,origin_part), axis = 0)
            calibrated = np.concatenate((calibrated, cali_part), axis = 0)
    print(origin)

# construction(result)
