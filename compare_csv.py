##Plots two time indexed temperature CSVs against each other and prints correlation
from datetime import datetime, timedelta

import pandas as pd
from dateutil.parser import parse


def pull_date(string_date):
    ##Returns a rounded datetime from a string
    try:
        date_time = datetime.strptime(string_date, "%H:%M %d/%m/%Y")
    except ValueError:
        try:
            date_time = parse(string_date)
        except ValueError:
            date_time = pd.NaT
            return date_time
    if date_time.second is not 0:
        if date_time.second >= 30:
            offset_seconds = timedelta(seconds=60 - date_time.second)
            date_time = date_time + offset_seconds
        else:
            offset_seconds = timedelta(seconds=date_time.second)
            date_time = date_time - offset_seconds
    return date_time


def convert_file(file):
    new_file = file + ".csv"
    old_file = file + ".txt"
    old = open(old_file, 'r')
    new = open(new_file, 'w')
    old.seek(0)
    lines = old.readlines()
    for line in lines:
        k = 0
        while True:
            i = line.find(':', k)
            j = line.find(',', k +i)
            if j < 0:
                ##Catches double line breaks such that
                ##csv has values on every line
                end = line.find('\n', k +i)
                if end > -1:
                    new.write(line[i + 2 : end])
                else:
                    new.write(line[i + 2:])
                break
            new.write(line[i + 2 : j + 1])
            k = j
    new.close()
    old.close()

def prep_csv(csv):
    try:
        file_chunks = pd.read_csv(csv + ".csv", header=None,
                                  iterator=True, chunksize=1000)
    except OSError:
        convert_file(csv)
        file_chunks = pd.read_csv(csv + ".csv", header=None,
                                  iterator=True, chunksize=1000)
    dataframe = pd.concat(file_chunks, ignore_index=True)
    s_date = dataframe[0]
    s_date = pd.Series([pull_date(date) for date in s_date])
    start = 0
    start_found = False
    while not start_found:
        if type(s_date[start]) is not pd.tslib.Timestamp:
            start += 1
        else:
            start_found = True
    end = s_date.size - s_date.count() - start
    if end:
        s_date = s_date[start : -end]
    else:
        s_date = s_date[start:]
    #Reset Keys
    s_date = pd.Series([x for x in s_date])
    s_temp = dataframe[1]
    if end:
        s_temp = s_temp[start : -end]
    else:
        s_temp = s_temp[start:]
    #Reset Keys
    s_temp = pd.Series([x for x in s_temp])
    dataframe_date = pd.DataFrame(s_date, columns=["date_time"])
    dataframe_temp = pd.DataFrame(s_temp, columns=["temp"])
    dataframe = dataframe_date.join(dataframe_temp)
    return dataframe


def interpolate(csv):
    dataframe = prep_csv(csv)
    start_time = dataframe["date_time"][0]
    end_time = dataframe["date_time"][dataframe.date_time.count() - 1]
    minutely = pd.date_range(start_time, end_time, freq="1min")
    minutelydataframe = pd.DataFrame(minutely, columns=["date_time"])
    dataframe = minutelydataframe.merge(dataframe, how="outer", on="date_time")
    dataframe.temp = dataframe.temp.interpolate()
    return dataframe


def compare_csv(f1, f2):
    dataframe1 = prep_csv(f1)
    dataframe2 = interpolate(f2)
    dataframe1 = dataframe1.rename(columns={"temp" : "temp1"})
    dataframe2 = dataframe2.rename(columns={"temp" : "temp2"})
    dataframe = dataframe1.merge(dataframe2, on="date_time")
    dataframe = dataframe.set_index(["date_time"])
    print("merged")
    print(dataframe)
    axis = dataframe.plot()
    figure = axis.get_figure()
    figure.savefig('temp.png')
    print('plotted')
    print(dataframe.corr())


def main():
    file1 = input('File 1 (Minutely): ')
    file2 = input('File 2 (Hourly): ')
    compare_csv(file1, file2)


if __name__ == '__main__':
    main()