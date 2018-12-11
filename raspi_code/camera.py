from time import sleep
from PIL import Image
import os

# This function crops the image to the desired dimension, so that the picture is on the spoon and the food on it only
# This is to remove the "noise" surroinding the sppon and increase our image recognition training and prediction accuracy
def crop_img(img_path, j, crop_ratio=1):

	# crop_ratio defines what is the size of the cropped image as a % of size of original 

	img = 'image_{}.jpg'.format(j)
	im = Image.open(img_path + img)
	
	f, e = os.path.splitext(img_path + img)
    
        #im.save(f + '.jpg', 'JPEG')
	#im.show()

	# Get dimensions
	width, height = im.size   

	#left = int(width * ((1 - crop_ratio) / 2))
	#top = int(height * ((1 - crop_ratio) / 2))
	#right = int(width * ((1 - crop_ratio) / 2 + crop_ratio))
	#bottom = int(height * ((1 - crop_ratio) / 2 + crop_ratio))
	
    # the settings below are hard-coded to ensure that the camera is focusing on the center of the spoon
    # where the food is being placed
	left = int(width) * 0.32
	right = int(width * 0.70)
	top = height * 0.13
	bottom = height * 0.94

	#print(left, right, top, bottom)

	cropped_im = im.crop((left, top, right, bottom))

	cropped_im.show()

	#cropped_im.save(f + '_cropped.jpg', 'JPEG')
	cropped_im.save(f + '.jpg', 'JPEG')

# This is a simple function to preview the image that will be taken on the Pi camera, take the picture and save the image.
def takePic(cam, j, img_path, crop_ratio=0.6):
    cam.start_preview()
    sleep(1)
    cam.capture(img_path + 'image_{}.jpg'.format(j))
    cam.stop_preview()
    crop_img(img_path, j, crop_ratio)
    #del camera
    #cam.close()
    
# This is a simple function to test the camera and make sure that it is properly calibrated to focus on the center of the spoon
#def test_cam():
#    from picamera import PiCamera
#    camera = PiCamera()
#    img_path =  '/home/pi/Desktop/'
#    takePic(camera, 8, img_path)
    
#test_cam()