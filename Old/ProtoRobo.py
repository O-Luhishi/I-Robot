
import RPi.GPIO as GPIO 	                                               # Import the GPIO module as 'GPIO'

import time                                                             # Import the 'time' module

import random

GPIO.setmode (GPIO.BCM)

output_ports = [26, 19, 23, 22, 27, 18, 17, 11]                         # Define the GPIO output port numbers
input_ports = [10, 9, 8, 7]                                             # Define the GPIO input port numbers

m1_en = 1                                                               # Motor 1 Enable (left motor)
m1_fwd = 2                                                              # Motor 1 Forward (left motor)
m1_rev = 4                                                              # Motor 1 Reverse (left motor)
m2_en = 8                                                               # Motor 2 Enable (right motor)
m2_fwd = 16                                                             # Motor 2 Forward (right motor)
m2_rev = 32                                                             # Motor 2 Reverse (right motor)

stop = 0                                                                # Drive value for no movement
left = m1_en + m1_rev + m2_en + m2_fwd                                  # Drive value for turning left
right = m1_en + m1_fwd + m2_en + m2_rev                                 # Drive value for turning right
fwd = m1_en + m1_fwd + m2_en + m2_fwd                                   # Drive value for moving forwards
rev = m1_en + m1_rev + m2_en + m2_rev                                   # Drive value for moving backwards

def motor_drive (value):                                                # Accept the motor drive value
    global input_ports, output_ports                                    # Allow acces to the assigned GPIO ports
    b = bin (value)                                                     # Create a binary string from the supplied value
    b = b [2:len(b)]                                                    # Strip off the '0b' from the start of the string
    b = b.zfill(8)                                                      # Make sure the string is eight bits long

    output_pointer = len (b) -1                                         # Start with the LSB of Binary string
    for port in output_ports:                                           # Pick out the individual GPIO port required
        output_state = int (b[output_pointer])                          # Select whether it needs to be on or off (1 or 0)
        GPIO.output (port,output_state)                                 # Turn on or off the relevant GPIO bit
        output_pointer = output_pointer - 1                             # Move to the next bit in the string
    for port in input_ports:                                            # Get the status of the four input bits
        b = str (GPIO.input (port)) + b                                 # Add the bit values to the Binary string
    return (b)                                                          # Exit with the Binary string in 'b'


def exit_program():
    z = motor_drive (False)                                             # Turn off all the GPIO outputs
    print ("\n\n")                                                      # Print a couple of blank lines
    GPIO.cleanup()                                                      # Clean up the GPIO ports
    exit()                                                              # And quit the program



for bit in output_ports:                                                # Set up the six output bits
    GPIO.setup (bit,GPIO.OUT)
    GPIO.output (bit,False)                                             # Initially turn them all off
    
for bit in input_ports:                                                 # Set up the six input bits
    GPIO.setup (bit,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)              # Set the inputs as normally low
    
while True:
#    direction = fwd 
    terminate = exit_program()

    movement = motor_drive (direction)                                  # Otherwise get the car moving (if needs be)

