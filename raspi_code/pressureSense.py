#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

# This function reads the pressure from the pressure sensor, as defined by the time it takes to charge the capacitor.
# The resistance across the pressure sensor decreases as more weight is placed on it, which reduces the amount of time it takes
# to charge the capacitor.  
def read_pressure(pin_to_circuit):
    count = 0
    # This threshold  is adjustable, and was set based on empirical tests.
    threshold = 50000
    #threshold = 4000000
                 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    # Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
        # Breaks out of the while loop once threshold is reached; this is when
        # there is nothing placed on the object. Including this  if statement avoids having to wait 
        # for the capacitor to fully charge even if nothing is placed on it.
        if count == threshold:
            break

    # If capacitor is charged quickly, meaning that an object is placed on it, we return True
    if count < threshold:
        item = True
    else:
        item = False

    return item, count


"""
while True:
    item, count = read_pressure(17)

    print("item = {}").format(item)
    print("count = {}").format(count)
    sleep(1)
"""