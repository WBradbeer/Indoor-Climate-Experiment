##Plots two time indexed temperature CSVs against each other and prints correlation
import pandas as pd
import numpy as np
import matplotlib as plt
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse

##Reformat date
def pullDate(strDate):
    try:
        dt = datetime.strptime(strDate, '%H:%M %d/%m/%Y')
    except ValueError:
        try:
            dt = parse(strDate)
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
    
def prepCSV(csv):
    names = ['date', 'temp', 'lights', 'knock']
    ##import csv in chunks
    fileChunks = pd.read_csv(csv, names=names, iterator=True, chunksize=1000)
    df = pd.concat(fileChunks, ignore_index=True)
    ##Get date as series and reformat date
    sD = df['date']
    sD = pd.Series([pullDate(date) for date in sD])
    ##Find Start and End of Data
    start = 0
    startFound = False
    while not startFound:
        if type(sD[start]) is not pd.tslib.Timestamp:
            start +=1
        else:
            startFound = True
    end = sD.size - sD.count() - start
    if (end):
        sD = sD[start:-end]
    else:
        sD = sD[start:]
    sD = pd.Series([x for x in sD])
    ##Get temp as series and reset indexes
    sT = df['temp']
    if (end):
        sT = sT[start:-end]
    else:
        sT = sT[start:]
    sT = pd.Series([x for x in sT])
    ##Make dataframes and join them
    dfD = pd.DataFrame(sD, columns = ['DateTime'])
    dfT = pd.DataFrame(sT, columns = ['Temp'])
    df = dfD.join(dfT)
    return df
    
def interpolate(csv):
    df = prepCSV(csv)
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
    
def compareCSV(f1, f2):
    df1 = prepCSV(f1)
    df2 = interpolate(f2)
    ##Make temp col have respective numbering
    df1 = df1.rename(columns = {'Temp':'temp1'})
    #print(df1)
    df2 = df2.rename(columns = {'Temp':'temp2'})
    #print(df2)
    ##Merge by Date Time
    df = df1.merge(df2, on="DateTime")
    df = df.set_index(['DateTime'])
    print('merged')
    #print(df)
    ##Plot together
    ax = df.plot()
    fig = ax.get_figure()
    fig.savefig('temp.png')
    print('plotted')
    print(df.corr())
     
f1 = input('File 1 (Minutely): ') + ".csv"
f2 = input('File 2 (Hourly): ') + ".csv"

compareCSV(f1, f2)
