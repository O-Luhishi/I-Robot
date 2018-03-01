#!/usr/bin/python
import sys
import Adafruit_DHT
import MySQLdb
import time
import DatabaseCollection
from datetime import datetime

class TemperatureAndHumidity():
    def __init__(self):
            pass
    def recordTempAndHumid(self):
        global humidity, temperature
        humidity, temperature = Adafruit_DHT.read_retry(11,4)


    def printTest(self):
        print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)


    def getHumidity(self):
        return humidity

    def getTemperature(self):
        return temperature

    def getTime(self):
        timeNow = datetime.now()
        return timeNow.strftime('%H:%M:%S')

    def getConstantStreamOfData(self):
        while True:
            #Code To Send Data To Database
            self.recordTempAndHumid()
            temp = DatabaseCollection.DataCollection()
            humid = DatabaseCollection.DataCollection()
            humid.sendValuesToDB("Light","lightvalues","addedwhen",self.getHumidity(),self.getTime())
            temp.sendValuesToDB("Temperature", "TemperatureValues","addedwhen",self.getTemperature(),self.getTime())
            time.sleep(2)



if __name__ == '__main__':
    Test1 = TemperatureAndHumidity()
    #Test1.recordTempAndHumid()
    Test1.getConstantStreamOfData()
    #print 'Humidity: ',Test1.getHumidity()
