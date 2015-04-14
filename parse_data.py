import xml.etree.ElementTree as ET
import glob

##Finds temperature and current time stamp for a given XML 
##Only works for citypage weather files
def getCurrentTemp(fileName):
    tree = ET.parse(fileName)
    root = tree.getroot()

    for currentConditions in root.findall('currentConditions'):
        time = currentConditions[1].find('hour').text + ":" + currentConditions[1].find('minute').text
        temp = currentConditions.find('temperature').text
        year = currentConditions[1].find('year').text
        month = currentConditions[1].find('month').text
        day = currentConditions[1].find('day').text
        
        textFile.write("Time: ")
        textFile.write(time)
        textFile.write(' ')
        textFile.write(day)
        textFile.write('/')
        textFile.write(month)
        textFile.write('/')
        textFile.write(year)
        textFile.write(", Temperature: ")
        textFile.write(temp)
        textFile.write('\n')
        textFile.flush()

textFile = open("parse.txt", 'w')
fileList = glob.glob("*xml")

##parses all XML in directory and formats data into one file
for file in fileList:
    getCurrentTemp(file)
    
   
textFile.close()