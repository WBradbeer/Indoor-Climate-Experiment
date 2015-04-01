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
    names = ['date', 'temp']
    ##import csv in chunks
    fileChunks = pd.read_csv(csv, names=names, iterator=True, chunksize=1000)
    df = pd.concat(fileChunks, ignore_index=True)
    
    ##Get date as series and reformat date
    s = df['date']
    s = s[3:-2]
    sD = pd.Series([pullDate(date) for date in s])
    ##Get temp as series and reset indexes
    s = df['temp']
    s = s[3:-2]
    sT = pd.Series([x for x in s])
    ##Make dataframes and join them
    dfD = pd.DataFrame(sD, columns = ['Date Time'])
    dfT = pd.DataFrame(sT, columns = ['Temp'])
    df = dfD.join(dfT)
    df = df.set_index(['Date Time'])
    return df
    
    
    
def compareCSV(f1, f2):
    df1 = prepCSV(f1)
    df2 = prepCSV(f2)
    ##Should check here to make sure both are date-time indexed
    ##Make temp col have respective numbering
    df1 = df1.rename(columns = {'Temp':'temp1'})
    #print(df1)
    df2 = df2.rename(columns = {'Temp':'temp2'})
    #print(df2)
    ##Merge by Date Time
    df = df1.join(df2)
    print('merged')
    #print(df)
    ##Plot together
    ax = df.plot()
    fig = ax.get_figure()
    fig.savefig('temp.png')
    print('plotted')
    print(df.corr())
     
f1 = input('File 1: ') + ".csv"
f2 = input('File 2: ') + ".csv"

compareCSV(f1, f2)