#!/usr/bin/python
import smbus
import time

class BH1750DCollector():
    global DEVICE, POWER_DOWN, POWER_DOWN, RESET, CONTINUOUS_LOW_RES_MODE
    global CONTINUOUS_HIGH_RES_MODE_1,CONTINUOUS_HIGH_RES_MODE_2
    global ONE_TIME_HIGH_RES_MODE_1, ONE_TIME_HIGH_RES_MODE_2
    global ONE_TIME_LOW_RES_MODE, bus, data

    # Default device I2C address
    DEVICE     = 0x23
    # No active states going on
    POWER_DOWN = 0x00
    # Power on
    POWER_ON   = 0x01
    # Reset data register value
    RESET      = 0x07
    # Start measurement at 4lx resolution. Time typically 16ms.
    CONTINUOUS_LOW_RES_MODE = 0x13
    # Start measurement at 1lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_1 = 0x10
    # Start measurement at 0.5lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_2 = 0x11
    # Start measurement at 1lx resolution. Time typically 120ms
    ONE_TIME_HIGH_RES_MODE_1 = 0x20
    # Start measurement at 0.5lx resolution. Time typically 120ms
    ONE_TIME_HIGH_RES_MODE_2 = 0x21
    # Start measurement at 1lx resolution. Time typically 120ms
    ONE_TIME_LOW_RES_MODE = 0x23
    # Rev Pi 2 V.b
    bus = smbus.SMBus(1)

    def __init__(self):
        pass

    def convertToNumber(self,data1):
      # Simple function to convert 2 bytes of data
      # into a decimal number
      return ((data1[1] + (256 * data1[0])) / 1.2)

    def readLight(self, addr=DEVICE):
      data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
      return str(self.convertToNumber(data))
