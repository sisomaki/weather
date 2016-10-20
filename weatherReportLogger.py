import logging


class weatherReportLogger:

    def __init__(self, debugLog=None):
        self.debugLog = logging.getLogger(__name__)

    def checkAlarm(self, location, weatherReport, logfile):
        for dailyreport in weatherReport:
            self.debugLog.debug("location: %s", location.location)
            self.debugLog.debug("2nd slot in wreport: %s", dailyreport[2])
            if(int(dailyreport[2]) > int(location.high_temp_alert)):
                self.debugLog.debug("High Alert Detected!")
                logfile.write("High Alert in location: " + location.location + ", on day " + str(dailyreport[1]) + ", with temp: " + str(dailyreport[2]) + "\n")
            if(int(dailyreport[3]) < int(location.low_temp_alert)):
                self.debugLog.debug("Low Alert detected!")
                logfile.write("Low Alert in location: " + location.location + ", on day " + str(dailyreport[1]) + ", with temp: " + str(dailyreport[3])+ "\n")


 
