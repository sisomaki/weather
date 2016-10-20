#!/usr/bin/python

import sys
import getopt
import time
import thread
import logging
import wundergroundservice
import weatherReportLogger
import weatherReportMonitoredLocation


def wuService(sleeptime, lock, key, locations, logfile):
    wus = wundergroundservice.wundergroundService()
    wrl = weatherReportLogger.weatherReportLogger()
    reportLog = logfile
    wreport = 0
    while 1:
        for loc in locations:
             lock.acquire()
             logging.debug('Location: %s', loc.location)
             logging.debug('Key: %s', key)
             wreport = wus.getWeatherForecast5dHighAndLow(key, loc.location)
             logging.debug('Weather Report Data for %s is: %s', loc.location, wreport) 
             reportLog.write("Location: " + loc.location + ", High: " + loc.high_temp_alert + ", Low: " + loc.low_temp_alert + "\n")
             lock.release()
             wrl.checkAlarm(loc, wreport, logfile)     
        logging.debug('Sleeping for: %s....', sleeptime)
        try:
            time.sleep(sleeptime)
        except KeyboardInterrupt:
            return


def main(argv):
    period = 0
    locations = []

    logging.basicConfig(filename='wu_prog.log', filemode='w', level=logging.DEBUG)

    lock = thread.allocate_lock()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:")
        logging.debug('Reading cmdline options')
    except getopt.GetoptError as e:
        print 'wu_prog.py -s <montoring_schedule> [-h for help]'
        logging.exception('Error reading cmdline options')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'wu_prog.py -s <monitoring_schedule> [-h for help]'
            sys.exit(2)
        elif opt == '-s':
            period = int(arg)
            logging.debug('user requested scheduling period is: %s', period)
            if(period < 60):
                period = 60
                logging.debug("changed period to 60 as minimum")
        else:
            print 'Usage: wu_prog.py -s <monitoring_schedule> [-h for help]'
            sys.exit(2)
    

    #
    #try:

    wuKeyFile = open('./wunderground.key', 'r')
    wuKey = str(wuKeyFile.readline()).strip()
    logging.debug('weather underground key in file is: %s', wuKey)
    #except 
      
    with open('./locations.txt', 'r') as locations_file:
        data = locations_file.readlines()
        for line in data:
            logging.debug('dataline: %s', line)
            words = line.split(',')
            stripped_words = map(str.strip, words)
            locations.append(weatherReportMonitoredLocation.weatherReportMonitoredLocation(stripped_words[0], stripped_words[2], stripped_words[1]))
        
        logging.debug('Monitored locations are: %s', locations)

    
    #thread.start_new_thread(wuService, period, lock, , logFile)
    reportlog = open('./userAlert.log', 'w')
    wuService(period , lock, wuKey, locations, reportlog)
    reportlog.close()
    logging.debug('closing app')

if __name__ == "__main__":
    main(sys.argv[1:])

