import csv
import codecs
from datetime import datetime
import numpy as np
import math
import argparse

def readfile(filename): #function for reading csv
    data = []
    with open(str(filename), encoding ='utf-16') as f:
        next(f) #skips header
        csvReader = csv.reader(f, delimiter='	', quoting=csv.QUOTE_NONNUMERIC)
        for row in csvReader:
            data.append(row)
        data = np.array(data) #converts to array
    return data

def newdata(arr_name, time_res,accu_interval): #function for generating  empty deaccumulated dataset
    mintime = min(data[:,0])
    maxtime = max(data[:,0])
    timedelta = maxtime - mintime 
    arr = np.zeros((int(timedelta/60/time_res+accu_interval*2/time_res),2), dtype=np.float)
    return arr, mintime, maxtime

def aug_data(arr,time_res,accu_interval): #function for augmenting/deaccumulation of data 
    new_arr, min_time, max_time = newdata(data,time_res,accu_interval)
    num_steps = int(accu_interval/time_res/2)
    for idx in range (len(new_arr)): # creates deaccumlated timestamps
        new_arr[idx,0] = min_time - accu_interval*60 + idx*time_res*60
    min_time_new = new_arr[0,0]
    for idx in range(len(arr)): # creates deaccumulated data
        timestamp = arr[idx, 0]
        newarr_idx = int((timestamp - min_time_new)/60/time_res-accu_interval/time_res)
        # data is deaccumulated by assuming a linear ramping up and down of rain which begins and ends the start and end of the 1 hour interval
        # the amount of rain at the peak is assumed to be twice the average rainfall pooled in the 1 hour interval 
        #the way the stepped curve is calculated, the value is slighly overestimated if larger time resolution used, 
        for time_idx in range(num_steps):
            new_arr[newarr_idx+time_idx,1] = arr[idx,1]*time_res*time_idx*2/(num_steps*accu_interval)
            new_arr[newarr_idx+num_steps+time_idx,1] = arr[idx,1]*time_res*2/(accu_interval)-arr[idx,1]*time_res*time_idx*2/(num_steps*accu_interval)
    return new_arr

def findmax(arr,period,time_res): #function for finding the maximum raindfall during the specified time requested
    #assumes maximium rainfall will occur at interval with single peak rainfall 
    #safe assumption given the consistency of type of data and deaccumulation model used 
    #this assumption saves abit of computation, has to change if new deaccumulation model or inconsistent data sources are added
    single_max_pos = np.argmax(arr[:,1]) 
    num_steps = math.ceil(period/time_res)
    temp_arr = np.zeros( (int(num_steps*time_res)), dtype=np.float)
    for idx in range(num_steps):
        for repeat_idx in range (int(time_res)):
            temp_arr[idx*int(time_res)+repeat_idx] = arr[single_max_pos+idx,1]/time_res
    total_max = sum(temp_arr[0:int(period)])
    max_time = arr[single_max_pos,0]
    return total_max, max_time

def writefile (arr,filename): #function for writing to new csv file 
    arr = arr.tolist()
    with open(str(filename)+".csv", 'w', encoding ='utf-16',) as f:
        csvwriter = csv.writer(f, delimiter="	")
        csvwriter.writerow(["unixtime",  "value"])
        np.savetxt(f, arr,'%F', delimiter="	")

if __name__ == "__main__": # e.g.  python .\script.py -f accumRainfall.csv -r 5 -p 30 -a 60
    #example script specifies the given csv file name, the 60 minute interval the data is pooled at, the 30 minutes peak data required, and a deaccumulation resolution of 5 minutes
    ap = argparse.ArgumentParser()
    ap.add_argument('-r', '--time_res', required=True, help="specify resolution of time in minutes required")
    ap.add_argument('-f', '--filepath', required=True, help="specify filepath of csv, including .csv")
    ap.add_argument('-p', '--period', required=True, help="specify period of time, in minutes, over which to find total maximum for")
    ap.add_argument('-a', '--accu_int', required=True, help="specify period of time, in minutes, which raw data is accumulated")
    args = ap.parse_args()

    data = readfile(str(args.filepath)) #read csv
    unaccum_data = aug_data(data,int(args.time_res),int(args.accu_int)) #deaccumulate data
    totalmax, maxtime = findmax(unaccum_data,int(args.period),int(args.time_res)) #find max rainfall in specified period and time which it occurs
    writefile(unaccum_data,'newfile') #writes new data to file
    print('highest rain fall in',args.period,'minutes') #based on the magnitude of the numbers, and geographical area it is from, unit is assumed to be in inches
    print(round(totalmax,4),'inches')
    print('Time which maximum rainfall occurs:') #time given in UTC
    print(datetime.fromtimestamp(int(maxtime)).strftime('%Y-%m-%d %H:%M:%S'),'UTC time')
