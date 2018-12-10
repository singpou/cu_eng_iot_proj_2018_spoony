# sudo apt-get update
# sudo pip install RPi.GPIO
# sudo apt-get install python-imaging python-smbus
# git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
# cd Adafruit_Python_SSD1306
# sudo python setup.py install

import time
import Adafruit_SSD1306
import Image
import ImageDraw
import ImageFont

# Raspberry Pi pin configuration:
RST = 24

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# # Note the following are only used with SPI:
# DC = 23
# SPI_PORT = 0
# SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:

def display_oled(cal_perc, bites):
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

    # Initialize library.
    disp.begin()
    disp.clear()
    disp.display()

    # Get display width and height.
    width = disp.width
    height = disp.height

    font = ImageFont.load_default()

    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    c = str(cal_perc)
    b = str(bites)
    draw.text((2,2), "{}% of your daily cal".format(c), font=font, fill=255)
    draw.text((2,20), "{} bites".format(b), font=font, fill=255)
    disp.image(image)

    # Display info
    disp.display()