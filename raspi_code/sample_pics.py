from time import sleep
from PIL import Image
import os

# This is a set of code which we ran to capture training images for our image recognition model.

def crop_img(img_path, j, crop_ratio=1):

	# crop_ratio defines what is the size of the cropped image as a % of size of original 

	img = 'image_{}.jpg'.format(j)
	im = Image.open(img_path + img)
	
	f, e = os.path.splitext(img_path + img)
    
        #im.save(f + '.jpg', 'JPEG')
	# im.show()

	# Get dimensions
	width, height = im.size   

	#left = int(width * ((1 - crop_ratio) / 2))
	#top = int(height * ((1 - crop_ratio) / 2))
	#right = int(width * ((1 - crop_ratio) / 2 + crop_ratio))
	#bottom = int(height * ((1 - crop_ratio) / 2 + crop_ratio))
	
	left = int(width) * 0.32
	right = int(width * 0.70)
	top = height * 0.13
	bottom = height * 0.94

	print(left, right, top, bottom)

	cropped_im = im.crop((left, top, right, bottom))

	cropped_im.show()

	#cropped_im.save(f + '_cropped.jpg', 'JPEG')
	cropped_im.save(f + '.jpg', 'JPEG')


def takePic(cam, j, img_path, crop_ratio=0.6):
    cam.start_preview()
    sleep(3)
    cam.capture(img_path + 'image_{}.jpg'.format(j))
    cam.stop_preview()
    crop_img(img_path, j, crop_ratio)
    #del cam
    
    
# test camera; we can increase/decrease the number of iterations depending on how many images
# we want to capture for each class of food
def test_cam():
    from picamera import PiCamera
    camera = PiCamera()
    for i in range(60):
        img_path =  '/home/pi/Desktop/bread/'
        takePic(camera, i, img_path)
    
test_cam()