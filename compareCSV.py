import pandas as pd
import numpy as np
import matplotlib as plt
from datetime import datetime

##Reformat date
def pullDate(strDate):
    dt = datetime.strptime(strDate, '%H:%M %d/%m/%Y')
    return dt
    
def prepCSV(csv):
    names = ['date', 'temp']
    ##import csv 
    df = pd.read_csv(csv, names=names)
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
    df2 = df2.rename(columns = {'Temp':'temp2'})
    ##Merge by Date Time
    df = df1.join(df2)
    print('merged')
    ##compare the two temperatures
    df.describe()
    df.corr()
    ##Plot together and save to file
    ax = df.plot()
    fig = ax.get_figure()
    fig.savefig('temp.png')
    print('plotted')
    
     
f1 = input('File 1: ')
f2 = input('File 2: ')

compareCSV(f1, f2)
