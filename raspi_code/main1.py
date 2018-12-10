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
# led to flash when calorie intake for the day is higher than a specified threshold
pressure_pin = 17
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

# simple fn to detect movement
def detect_mm(x, y, mv_threshold):
    if x * y < 0 and np.absolute(x - y) > mv_threshold:
        return True
    else:
        return False

def adxl_hang(x, y):
    if x == 0.0 and y == 0.0:
        return True
    else:
        return False


# main while loop
while True:

    axes = adxl345.getAxes(True)    
    x = axes['x']
    y = axes['y']
    
    print("x:", x , "y:", y)

    items = np.roll(items, 1)
    print("Detecting presence of object...")
    item, count = read_pressure(pressure_pin)
    
    if item:
        items[0] = 1.0
    else:
        items[0] = 0
        
    print(items)
    
    obj_detected = np.max(items) == 1.0
    
    if detect_mm(x, y, mv_threshold):

        sleep(0.5)
        # if item detected on pressure sensor
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
            
            if cal_perc >= cal_threshold1 and cal_perc < cal_threshold2:
                flash_led(led_pin, 1)
            elif cal_perc >= cal_threshold2:
                flash_led(led_pin, 2)           
            
            
            display_oled(cal_perc, bites)
            
            img_idx += 1
        
        # Re-create the accelerometer object as it is deleted
        # when we do not read from it
        
        
        adxl345 = ADXL345()
                    
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    if adxl_hang(x, y):
        print("restart adxl345")
        adxl345 = ADXL345()
    
    sleep(0.5)