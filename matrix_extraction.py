#
# functions to deal with arrington eyetracking data
#
import pandas as pd
import re

# --- read in a calibration file
# adapted from perl:
# BEGIN{$event="NA\\tNA"}
#  $event="$F[2]\\t$F[1]" if/^12/;
#  print join("\\t",@F[1..12],$event) if m/^10/'
def read_arrington(eyefile):
    with open(eyefile) as f:
        event = None
        event_time = 0
        data = []
        for line in f:
            v = line.split()
            if len(v) == 0: continue
            # line starts with 10, it's data
            #                  12, it's event info
            if v[0] == "10":
                data.append(
                    [float( re.sub(',.*','',x) )
                      for x in v[1:13] ] +
                    [event, event_time])
            elif v[0] == "12":
                event = v[2]
                event_time = float(v[1])
            else:
                pass
                # print("Bad line " + line)

    df = pd.DataFrame(data)
    df.columns = ["totaltime", "deltatime",
                  "x_gaze", "y_gaze", "x_correctedgaze", "y_correctedgaze",
                  "region", "pupilwidth", "pupilheight", "quality",
                  "fixation", "count", "event_str", "event_onset"]
    return(df)


def et_3part_trigger(df):
    # event like ["fix_center_0.5", "look_Left_-0.605...",...] =>
    #  separate columns, pos should be numeric

    df['action'], df['side'], df['pos'] = df['event_str'].str.split('_', 2).str
    df['pos'] = df['pos'].replace('None', pd.np.Inf).astype('float')

    # show box plot of each positions
    df = prepare_for_plot(df)

    return(df)

# specifically for mri_eyecal.py
def add_cal_timing(tfile,df):
    firstrow= pd.DataFrame([0])
    event = pd.read_table(tfile,sep=" ",header=None)
    t = firstrow.append(event,ignore_index=True)

    # reset to when we resume form pause
    unpauseidx = pd.np.where(df['totaltime'].diff()>.02)[0]
    if len(unpauseidx)>0:
        df['adjtime'] = df['totaltime'] - df['totaltime'][unpauseidx[0]]

    j=0; lasti=0
    df['pos'] = pd.np.NaN
    df['event_onset'] = pd.np.NaN
    for i in range(0,t.shape[0]-1):
        time=t[0][i+1]
        pos=t[1][i]
        #print(i,j,time, '>=', df['adjtime'][j],"init")
        while j < df.shape[0]-1 and time >= df['adjtime'][j]:
            #print(i,j,time,'>=', df['adjtime'][j], 'set ',pos)
            df.loc[j,'pos'] = pos
            df.loc[j,'event_onset'] = t[0][i]
            lasti=i
            j+=1
    # set last
    df['pos'][j:]=t[1][lasti+1]
    df['event_onset'][j:] = t[0][lasti+1]
    # set side
    df['side'] = [ 'right' if x > 0 else 'left' for x in df['pos'] ]
    df.loc[df['pos']==0,'side'] = 'center'
    # same as in et_3part_trigger(df)
    df = prepare_for_plot(df)
    return(df)

def prepare_for_plot(df):
    df['pos'] = ["%.02f" % x for x in df['pos']]
    df = df.query('pos not in ["nan", "inf"] ')
    df['onset_rank'] = df.\
        groupby('pos')['event_onset'].\
        rank(method="dense").\
        astype(int)
    df.loc[df.onset_rank >= 3, 'onset_rank'] = 3
    return(df)
