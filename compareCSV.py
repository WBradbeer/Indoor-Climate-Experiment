##Plots two time indexed temperature CSVs against each other and prints correlation
import pandas as pd
import numpy as np
import matplotlib as plt
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse


def pull_date(string_date):
    ##Returns a rounded datetime from a string 
    try:
        dt = datetime.strptime(string_date, '%H:%M %d/%m/%Y')
    except ValueError:
        try:
            dt = parse(string_date)
        except ValueError:
            dt = pd.NaT
            return dt
    if (dt.second !=0):
        if (dt.second >= 30):
            td = timedelta(seconds = 60 - dt.second)
            dt = dt + td
        else:
            td = timedelta(seconds = dt.second)
            dt = dt - td  
    return dt
    
def convert_file(file):
    new_file = file + ".csv"
    old_file = file + ".txt"
    old = open(old_file, 'r')
    new = open(new_file, 'w')
    ##Find start and read       
    old.seek(0)
    lines = old.readlines()
    ##Write lines in csv format       
    for line in lines:
        k = 0;
        for col in range(3):
            ##print(k)
            i = line.find(':', k)
            ##print(i)
            j = line.find(',', k +i)
            if j<0:
                ##Catches double line breaks such that csv has values on every line
                end = line.find('\n', k +i)
                if end > -1:
                    new.write(line[i+2:end])
                else:
                    new.write(line[i+2:])
                break
            ##print(j)
            new.write(line[i+2:j+1])
            k= j      
                
    new.close()
    old.close()
    
def prep_csv(csv):
    ##import csv in chunks
    try:
        file_chunks = pd.read_csv(csv + ".csv", header=None, iterator=True, chunksize=1000)
    except OSError:
        convert_file(csv)
        file_chunks = pd.read_csv(csv + ".csv", header=None, iterator=True, chunksize=1000)
        
    df = pd.concat(file_chunks, ignore_index=True)
    ##Get date as series and reformat date
    s_date = df[0]
    s_date = pd.Series([pull_date(date) for date in s_date])
    ##Find Start and End of Data
    start = 0
    start_found = False
    while not start_found:
        if type(s_date[start]) is not pd.tslib.Timestamp:
            start +=1
        else:
            start_found = True
    end = s_date.size - s_date.count() - start
    if end:
        s_date = s_date[start:-end]
    else:
        s_date = s_date[start:]
    s_date = pd.Series([x for x in s_date])
    ##Get temp as series and reset indexes
    s_temp = df[1]
    if end:
        s_temp = s_temp[start:-end]
    else:
        s_temp = s_temp[start:]
    s_temp = pd.Series([x for x in s_temp])
    ##Make dataframes and join them
    df_date = pd.DataFrame(s_date, columns = ['DateTime'])
    df_temp = pd.DataFrame(s_temp, columns = ['Temp'])
    df = df_date.join(df_temp)
    return df
    
def interpolate(csv):
    df = prep_csv(csv)
    #create minutely series
    startTime = df['DateTime'][0]
    endTime = df['DateTime'][df.DateTime.count()-1]
    minutely = pd.date_range(startTime, endTime, freq='1min')
    #Merge with temp data
    minutelydf = pd.DataFrame(minutely, columns = ["DateTime"])
    df= minutelydf.merge(df, how ="outer", on = "DateTime")
    #interpolate linearly
    df.Temp = df.Temp.interpolate()
    return df    
    
def compare_csv(f1, f2):
    df1 = prep_csv(f1)
    df2 = interpolate(f2)
    ##Make temp col have respective numbering
    df1 = df1.rename(columns = {'Temp':'temp1'})
    print(df1)
    df2 = df2.rename(columns = {'Temp':'temp2'})
    print(df2)
    ##Merge by Date Time
    df = df1.merge(df2, on="DateTime")
    df = df.set_index(['DateTime'])
    print('merged')
    print(df)
    ##Plot together
    ax = df.plot()
    fig = ax.get_figure()
    fig.savefig('temp.png')
    print('plotted')
    print(df.corr())
     
f1 = input('File 1 (Minutely): ') 
f2 = input('File 2 (Hourly): ') 

compare_csv(f1, f2)
