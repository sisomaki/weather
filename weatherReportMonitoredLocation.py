import logging

class weatherReportMonitoredLocation(object):
    def __init__(self, Location=None, HighAlertTemp=None, LowAlertTemp=None):
       self.location = Location
       self.high_temp_alert = HighAlertTemp
       self.low_temp_alert = LowAlertTemp
       logger = logging.getLogger(__name__)
       logger.debug('Location: %s, HighTemp: %s, LowTemp: %s', self.location, self.high_temp_alert, self.low_temp_alert)

 
