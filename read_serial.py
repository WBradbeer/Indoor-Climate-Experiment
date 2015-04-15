import serial 
import time 

#Header is required for time stamp to be read by arduino
header = "T"

def send_time_stamp(header, time):
    time_string = str(t)
    time_stamp = header + time_string
    ser.write(time_stamp.encode())


def main():    
    connected = False
    #Open Arduino Serial Port and loop until arduino is ready
    ser = serial.Serial("COM4", 9600)   
    while not connected:
        serin = ser.read()
        connected = True

    epoch_time = time.time()
    send_time_stamp(Header, epoch_time)

    text_file = open("read.txt", 'w')
    current_time = str(time.ctime())
    text_file.write("********************")
    text_file.write('Started reading serial at: ')
    text_file.write(current_time)
    text_file.write("********************")

    while 1:
        if ser.inWaiting():
            x=ser.read()
            x= x.decode("utf-8")
            print(x)
            text_file.write(x)
            text_file.flush()
    text_file.close()
    ser.close()

if __name__ == '__main__':
    main()