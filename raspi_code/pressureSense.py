#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

#define the pin that goes to the circuit
#pin_to_circuit = 17

def read_pressure(pin_to_circuit):
    count = 0
    threshold = 50000
    #threshold = 4000000
                 
    #define the pin that goes to the circuit
    #pin_to_circuit = 17
    #Output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
        if count == threshold:
            break
            
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