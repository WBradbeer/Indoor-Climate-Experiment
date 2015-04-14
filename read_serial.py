import serial 
import time 
##Header required fir time stamp
Header = "T"

##Writes current time to Arduino
def sendTimeStamp(header, time):
    timeStr = str(t)
    timeStamp = header + timeStr
    ser.write(timeStamp.encode())
    
## Boolean for whether Arduino is connected
connected = False

##Open Arduino Serial Port
ser = serial.Serial("COM4", 9600)
  

##Loop until Arduino is ready
while not connected:
    serin = ser.read()
    connected = True
##Gives seconds from 1970 to current time UTC 
t = time.time()
sendTimeStamp(Header, t)    
    
##Open text file
textFile = open("read.txt", 'w')
currentTime = str(time.ctime())
textFile.write("********************")
textFile.write('Started reading serial at: ')
textFile.write(currentTime)
textFile.write("********************")

##read serial to text file
while 1:
    if ser.inWaiting():
        x=ser.read()
        x= x.decode("utf-8")
        print(x)
        textFile.write(x)
        textFile.flush()
	

textFile.close()
ser.close()
