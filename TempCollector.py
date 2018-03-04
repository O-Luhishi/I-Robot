#!/usr/bin/python
import sys
import Adafruit_DHT
import MySQLdb
import time
import DatabaseCollection
import BH1750
from datetime import datetime

class SensorCollector():
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


    def getLightIndex(self):
        lightValue = BH1750.BH1750DCollector()
        return lightValue.readLight()

    def getTime(self):
        timeNow = datetime.now()
        return timeNow.strftime('%H:%M:%S')

    def getConstantStreamOfData(self):
        while True:
            #Code To Send Data To Database
            self.recordTempAndHumid()
            temp = DatabaseCollection.DataCollection()
            humid = DatabaseCollection.DataCollection()
            light = DatabaseCollection.DataCollection()

            light.sendValuesToDB("Light","lightvalues","addedwhen",self.getLightIndex(),self.getTime())
            temp.sendValuesToDB("Temperature", "TemperatureValues","addedwhen",self.getTemperature(),self.getTime())
            humid.sendValuesToDB("Humidity", "HumidityValues", "addedwhen", self.getHumidity(), self.getTime())
            time.sleep(1)



if __name__ == '__main__':
    Test1 = SensorCollector()
    Test1.getConstantStreamOfData()
