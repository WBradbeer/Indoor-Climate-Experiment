from urllib import request
import sched, time

##Downloads a specific URL with filename based on time
def download_xml(URL, filename):
    download = request.URLopener()
    download.retrieve(URL, filename + str(time.time()) + ".xml")
    print("File downloaded at ")
    print(time.gmtime())
    print(" UTC")


##Downloads a common URL at specified time intervals
def scheduled_download(url, interval, count):
    schedule = sched.scheduler(time.time, time.sleep)
    for j in range(count):
        schedule.enter(interval*j,1,download_xml, (url, 'Data' ))
    schedule.run()


def main():
    url = "http://dd.weather.gc.ca/citypage_weather/xml/ON/s0000430_e.xml"
    scheduled_download(url, 3600, 24)


if __name__ == '__main__':
    main()