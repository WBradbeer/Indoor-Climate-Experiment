##expands hourly time data to minutely without interpolation
import time

def expandFile(oldFile, newFile):
    old = open(oldFile, 'r')
    new = open(newFile, 'w')
    
    currentTime = str(time.ctime())
    new.write("********************\n")
    new.write('Started expanding file at: ')
    new.write(currentTime)
    new.write("\n********************\n")
    new.flush()
    
    old.seek(0)
    lines = old.readlines()
    for line in lines:
        for row in range(60):
            i = line.find(',')
            if (i > 0):
                if (row < 10):
                    new.write(line[:i-1])
                else: 
                    new.write(line[:i-2])
                new.write(str(row))
                new.write(line[i:])
                new.flush()
            else:
                new.write(line)
                new.flush()
                break
    currentTime = str(time.ctime())
    new.write("********************\n")
    new.write('Finished expanding file at: ')
    new.write(currentTime)
    new.write("\n********************\n")
    new.flush()
    
    new.close()
    old.close()
    
oldName = input('Old Name: ')
newName = oldName + 'EX'

expandFile(oldName + '.csv', newName + '.csv')

