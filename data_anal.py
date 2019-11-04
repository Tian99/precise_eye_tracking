import pickle
import matplotlib.pyplot as plt

trim_bound = 46


#Analyze the data using histgram
def trim(pickle):
    pickle_new = []
    for i in pickle:
        i = {k:v for k,v in i.items() if k >= trim_bound}
        print(i)

        if i != None:
            pickle_new.append(i)

    return pickle_new

def line(pickle):
    lis_x = []
    lis_y = []
    lis_r = []
    lis_v = []
    for i in pickle:
        item = i.items()
        for j in item:
            #j = (4, [19, 82, 20])
            lis_v.append([j[0]])
            lis_x.append(j[1][0])
            lis_y.append(j[1][1])
            lis_r.append(j[1][2])
    plt.scatter(lis_x, lis_y)
    plt.show()

def hist(pickle):
    lis_x = []
    lis_y = []
    lis_r = []
    for i in pickle:
        item = i.items()
        for j in item:
            # print(j)
            #j = (4, [19, 82, 20])
            lis_x.append(j[1][0])
            lis_y.append(j[1][1])
            lis_r.append(j[1][2])

    plt.hist(lis_x, bins = 500)

    plt.show()



f = open('data/dict.pickle', 'rb')    
pickle =  pickle.load(f) 
pickle = trim(pickle)
line(pickle) 
