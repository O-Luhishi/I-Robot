import RPi.GPIO as gpio
import time

def init():
	gpio.setmode(gpio.BCM)
	gpio.setup(24, gpio.OUT)
#	gpio.setup(23, gpio.OUT)
#	gpio.setup(23, gpio.OUT)
#	gpio.setup(24, gpio.OUT)

def forward(tf):
	init()
	gpio.output(24, True)
#	gpio.output(23, False)
#	gpio.output(23, True)
#	gpio.output(24, False)
	time.sleep(tf)
	gpio.cleanup()


print "forward"
forward(4)
