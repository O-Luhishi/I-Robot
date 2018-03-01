
import RPi.GPIO as GPIO 	                                               # Import the GPIO module as 'GPIO'
import cwiid
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
right = m1_en + m1_rev + m2_en + m2_fwd                                  # Drive value for turning left
left = m1_en + m1_fwd + m2_en + m2_rev                                 # Drive value for turning right
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
    

print ("\n\n\n\nPress 1 & 2 together on your Wii Remote now ...")       # Print some instructions

attempt = ['first', 'second', 'last']                                   # Make them a bit informative
word = 0                                                                # Number of attempts to connect
while True:                                                             # Start an infinite loop
    try:
        print ("\n\nTrying to connect for the"), attempt [word],
        print ("time...\n\nAttempt"), word+1                            # Print current attempt
    
        wii=cwiid.Wiimote()                                             # Wait for a response from the Wii remote
        break                                                           # If successful then exit the loop

    except RuntimeError:                                                # If it times out...
        word = word + 1                                                 # Try again
        if word == 3:                                                   # If it fails after 3 attempts...
            print ("\n\nFailed to connect to the Wii remote control")   # Print a failure message
            print ("\nProgram Terminated\n")
            print ("Please restart the program to begin again\n\n")

            terminate = exit_program()                                  # And exit the program

wii.rumble = 1                                                          # Briefly vibrate the Wii remote
time.sleep(0.2)
wii.rumble = 0
wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC                            # Report button and accelerometer data

print ("\n\n\n\nThe Wii Remote is now connected...\n")                  # Print a few instructions
print ("Use the direction pad to steer the car\n")
print ("or...\n")
print ("Hold the 'B' button and tilt the Wii Remote to steer\n")
print ("or...\n")
print ("Press and hold down the 'A' button for Autonomous Mode\n")
print ("Press '+' and '-' buttons at the same time quit.\n")

while True:                                                             # Begin an infinite loop
    direction = stop                                                    # Set the initial direction to none (stop)
    buttons = wii.state['buttons']                                      # Get the button data from the Wii remote
    x, y, z = wii.state['acc']                                          # Also get the accelerometer data
    if not (buttons & cwiid.BTN_B):                                     # Only use accelerometer data if
        x, y, z = 125, 125, 125                                         # the 'B' button is being pressed

    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):               # Are both the '+' and '-' buttons pressed?
        print ("\nThe Wii Remote connection has been closed\n")
        print ("Please restart the program to begin again\n")           # Yes - Print a message
        wii.rumble = 1                                                  # Briefly vibrate the Wii remote
        time.sleep(0.2)
        wii.rumble = 0
        terminate = exit_program()                                      # And quit the program

    if (buttons - cwiid.BTN_A == 0):                                    # If ONLY the 'A' button is pressed
        movement = automatic (buttons)                                  # then run autonomously

    if (buttons & cwiid.BTN_LEFT) or x < 110:
        direction = left                                                # Prepare to turn the car to the left

    if(buttons & cwiid.BTN_RIGHT) or x > 130:
        direction = right                                               # Prepare to turn the car to the right

    if (buttons & cwiid.BTN_UP) or y > 130:
        direction = fwd                                                 # Prepare to drive the car forwards
    
    if (buttons & cwiid.BTN_DOWN) or y < 110:
        direction = rev

    movement = motor_drive(direction)
