import time

def convertFile(oldFile, newFile):
    old = open(oldFile, 'r')
    new = open(newFile, 'w')
    
    currentTime = str(time.ctime())
    new.write("********************\n")
    new.write('Started converting file at: ')
    new.write(currentTime)
    new.write("\n********************\n")

    
    old.seek(0)
    lines = old.readlines()
    
       
    for line in lines:
        k = 0;
        for col in range(3):
            ##print(k)
            i = line.find(':', k)
            ##print(i)
            j = line.find(',', k +i)
            if (j<0):
                ##Catches double line breaks such that csv has values on every line
                end = line.find('\n', k +i)
                if (end > -1):
                    new.write(line[i+2:end])
                else:
                    new.write(line[i+2:])
                break
            ##print(j)
            new.write(line[i+2:j+1])
            k= j
            
        
                
    currentTime = str(time.ctime())
    new.write("********************\n")
    new.write('Finished converting file at: ')
    new.write(currentTime)
    new.write("\n********************")
    
    new.close()
    old.close()
    
oldName = str(raw_input('Old Name: '))
newName = str(raw_input('New Name: '))

convertFile(oldName + '.txt', newName + '.csv')