from time import sleep
import numpy as np
import time

# for accelerometer
from adxl345 import ADXL345

#enable pressure sensor
import RPi.GPIO as GPIO
from pressureSense import read_pressure

# for temperature sensor
from temperaturesensor import read_temp

# for camera
from picamera import PiCamera
cam = PiCamera()
from camera import takePic

# for sending to server
from send_to_server import send_data

server_url = "http://34.201.135.161:4028/"

# for led
from led import flash_led

# for oled
from oled import display_oled

# initialize settings for pressure sensor
pressure_pin = 17

# items is the spoon's memory to recall if an object was placed on the spoon recently. 
# The reason for keeping a memory is so that we can check the memory when we detect movmenet via the accelerometer. If nothing 
# was placed on the spoon, it will not take further action.
# We can increase its memory simply by increasing the length of this numpy array.
items = np.zeros(5)

 # initialize settings for led
# led to flash when calorie intake for the day is higher than a specified threshold
led_pin = 14
cal_threshold1 = 75
cal_threshold2 = 100
# flash = False

# initialize settings for camera
img_idx = 0
img_path =  '../images/'
# crop ratio is the size of cropped img as % of original
crop_ratio = 0.6

# initialize settings for accelerometer
GPIO.setmode(GPIO.BCM)
adxl345 = ADXL345()

# initialize settings for calculating moving average of accelerometer readings
win_size = 5
x_mov_win = np.zeros(win_size)
y_mov_win = np.zeros(win_size)
counter = 0
mv_threshold = 0.01

# simple fn to detect movement via  the accelerometer
def detect_mm(x, y, mv_threshold):
    if x * y < 0 and np.absolute(x - y) > mv_threshold:
        return True
    else:
        return False

# the ADXL may sometimes "hang" and when that happens x and y readings go to 0.0;
# this function sets the flag for resetting the adxl to ensure that the spoon can continue to operate.
def adxl_hang(x, y):
    if x == 0.0 and y == 0.0:
        return True
    else:
        return False

# main while loop
while True:

    # Take in the x and y readings from the accelerometer
    axes = adxl345.getAxes(True)    
    x = axes['x']
    y = axes['y']
    
    print("x:", x , "y:", y)
    
    # We keep a moving window of the memory
    items = np.roll(items, 1)
    print("Detecting presence of object...")
    # read_pressure reads the reading from the pressure sensor to detect if an object was placed on the spoon 
    item, count = read_pressure(pressure_pin)
    
    # Update the memory 
    if item:
        items[0] = 1.0
    else:
        items[0] = 0
        
    print(items)
    
    # If an object was placed on the spoon in recent memory, we consider it that an object is now on the spoon
    obj_detected = np.max(items) == 1.0
    
    # If movement is detected by the accelerometer
    if detect_mm(x, y, mv_threshold):

        sleep(0.5)
        # if item is detected on pressure sensor as recalled by the memory
        if obj_detected:
            #pin_to_circuit = 17
            print("Object detected! Time it took to charge capacitor:", count)
            print("Reading temperature...")
            temp = read_temp()
            
            print("Temperature is ", temp)
            print("Taking Picture")
            takePic(cam, img_idx, img_path, crop_ratio)
            cal_perc, bites = send_data(temp, img_idx, server_url)
            print("Sending Picture...")
            
            #cal_perc = 120
            #bites = 300

            # If calorie intake is  more than threshold, light the LED up to nudge the user 
            if cal_perc >= cal_threshold1 and cal_perc < cal_threshold2:
                flash_led(led_pin, 1)
            elif cal_perc >= cal_threshold2:
                flash_led(led_pin, 2)           
            
            # Inform the user via the OLED how many calories and bites of food he/she has taken 
            display_oled(cal_perc, bites)
            
            img_idx += 1
        
        # Re-create the accelerometer object as it is deleted
        # when we do not read from it
        adxl345 = ADXL345()

    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    # Restarts the accelerometer if it hangs to ensure that the spoon continues to operate smoothly
    if adxl_hang(x, y):
        print("restart adxl345")
        adxl345 = ADXL345()
    
    sleep(0.5)