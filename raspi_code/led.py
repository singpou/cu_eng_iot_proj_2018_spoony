#!/usr/local/bin/python
# 
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

# Defines the number of times that the LED should flash when the calorie intake exceeds 100% of the daily recommended dosage.
cycles_for_cal100 = 3

# This function sets up the LED which serves to nudge the user towards a healthier diet, by telling him/her that
# he has eaten beyond a certain level of his daily recommended calorie intake
def flash_led(led_pin, threshold_num):
    
    GPIO.setup(led_pin, GPIO.OUT)
    
    # threshold 1 is when calorie intake is >75%; light up LED for 3 seconds 
    if threshold_num == 1:
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(3)
    # threshold 2 is when calorie intake is >100%; flash LED 3 times
    elif threshold_num == 2:
        #print("100")
        for i in range(cycles_for_cal100):
            GPIO.output(led_pin, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(0.5)
