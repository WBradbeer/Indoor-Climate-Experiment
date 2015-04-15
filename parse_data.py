import xml.etree.ElementTree as ET
import glob

##Finds temperature and current time stamp for a given XML 
##Only works for citypage weather files
def get_current_temp(fileName):
    tree = ET.parse(fileName)
    root = tree.getroot()
    for current_conditions in root.findall('current_conditions'):
        time = current_conditions[1].find('hour').text + ":" + current_conditions[1].find('minute').text
        temp = current_conditions.find('temperature').text
        year = current_conditions[1].find('year').text
        month = current_conditions[1].find('month').text
        day = current_conditions[1].find('day').text
        #Format Date to parse-able format 
        text_file.write("Time: ")
        text_file.write(time)
        text_file.write(' ')
        text_file.write(day)
        text_file.write('/')
        text_file.write(month)
        text_file.write('/')
        text_file.write(year)
        text_file.write(", Temperature: ")
        text_file.write(temp)
        text_file.write('\n')
        text_file.flush()


def main():
    text_file = open("parse.txt", 'w')
    file_list = glob.glob("*xml")
    for file in file_list:
        get_current_temp(file) 
    text_file.close()


if __name__ == '__main__':
    main()