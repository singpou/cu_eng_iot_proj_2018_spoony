#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

cycles_for_cal100 = 3

#define the pin that goes to the circuit
def flash_led(led_pin, threshold_num):
    #Output on the pin for
    
    GPIO.setup(led_pin, GPIO.OUT)
    
    if threshold_num == 1:
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(3)
    elif threshold_num == 2:
        print("100")
        for i in range(cycles_for_cal100):
            GPIO.output(led_pin, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(0.5)
