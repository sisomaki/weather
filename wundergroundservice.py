#wundergroundservice.py
#class that handles the weather underground service connection and data
#requires requests library
import sys
import logging
import requests
import copy

class wundergroundService:    

    def __init__(self, debugLog=None):
        self.debugLog = logging.getLogger(__name__)
    
    def get10dWeatherForecast(self, key, location):
            url = 'http://api.wunderground.com/api/' + key + '/geolookup/forecast10day/q/' + location + '.json'
            self.debugLog.debug("Using wunderground key: %s for location: %s.", key, location)
            
            # need to check for network errors
            try:
                r = requests.get(url)
                j = r.json()
                self.debugLog.debug(j)
            except:
                self.debugLog.debug("Network Error in fetching weather data")
                sys.exit(-1)
            return j


    def getWeatherForecast5dHighAndLow(self, key, location):
            dailyforecast = []
            f = []
            forecastHighAndLow = []

            weatherData = self.get10dWeatherForecast(key, location)
            self.debugLog.debug('Forecast 1st day is: %s', weatherData['forecast']['simpleforecast']['forecastday'])

            for day in weatherData['forecast']['simpleforecast']['forecastday']:
                self.debugLog.debug('Day: %s, High temp: %s C, Low temp: %s C', day['date']['weekday'], day['high']['celsius'], day['low']['celsius'])
                dailyforecast[:] = []
                #prepare the array of data
                dailyforecast.append(str(day['date']['weekday']))
                dailyforecast.append(int(day['period']))
                dailyforecast.append(int(day['high']['celsius']))
                dailyforecast.append(int(day['low']['celsius']))
                self.debugLog.debug('Daily Forecast is: %s', dailyforecast)
                f = copy.deepcopy(dailyforecast)
                forecastHighAndLow.append(f)
                self.debugLog.debug(forecastHighAndLow)
                if int(day['period']) >= 5:
                    self.debugLog.debug('5th day encountered')
                    break

            return forecastHighAndLow

