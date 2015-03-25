from urllib import request
import sched, time

##Downloads a specific URL with filename based on time
def downloadXML(URL, filename):
    dl = request.URLopener()
    dl.retrieve(URL, filename + str(time.time()) + ".xml")
    print("File downloaded at ")
    print(time.gmtime())
    print(" UTC")
    
url = "http://dd.weather.gc.ca/citypage_weather/xml/ON/s0000430_e.xml"

    
s = sched.scheduler(time.time, time.sleep)

##Downloads a common URL at specified time intervals
def scheduledDownload(url, interval, count):
    for j in range(count):
        s.enter(interval*j,1,downloadXML, (url, 'Data' ))
    s.run()
    

scheduledDownload(url, 3600, 24)

