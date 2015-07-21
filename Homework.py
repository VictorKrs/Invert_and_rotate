import argparse
import os
from PIL import Image

#------ FUNCTIONS --------

def image_list (path):
# Create list of images
	file_list = os.listdir(path = '.')
	jpg_list = list(filter(lambda x: x.endswith('.jpg'), file_list))   # list of .jpg format
	png_list = list(filter(lambda x: x.endswith('.png'), file_list))   # list of .png format
	list_of_im = [jpg_list, png_list]
	return list_of_im

def im_rotate(name, grad):
# Rotate picture on 'grad' degrees
        im = Image.open(name)
        im.rotate(grad).save(name)
        im.close()

def inv_im(name, rgb):
# Invert image
        im = Image.open(name)
        pixels = im.load()    # all pixels of image
        size = im.size        # size of image

        # invert
        for i in range(size[0]):
                for j in range(size[1]):
                        pixel = pixels[i, j]
                        if rgb['r']: pixel = (255 - pixel[0], pixel[1], pixel[2])    # invert red color
                        if rgb['g']: pixel = (pixel[0], 255 - pixel[1], pixel[2])    # invert green color
                        if rgb['b']: pixel = (pixel[0], pixel[1], 255 - pixel[2])    # invert blue color
                        pixels[i, j] = pixel

        im.save(name)
        im.close()

def conv_im(name, grad, rgb):
# Convert image
        # create copy of image
        try: im = Image.open(name)
        except OSError:      # if image don't open
                pass
        else:                # if image open
                name_copy = 'copy_' + name
                im.save(name_copy)
                im.close()

                # invert image
                if rgb['flag']:                
                        inv_im(name_copy, rgb)

                im_rotate(name_copy, grad)    # rotate image     

def conv_images(path, grad, inv):
# Convert images with .jpg or .png formats
        try: os.chdir(path)		# change directory
        except FileNotFoundError:       # directory not found
                print("ERROR: Directory not found")
        else:
                # lists of images
                list_of_im = image_list(path)	
                jpg_list = list_of_im[0]	# list of .jpg format
                png_list = list_of_im[1]	# list of .png format

                # map of invert parametrs (RGB)
                rgb = {'r' : 0, 'g' : 0, 'b' : 0}   # 1 - need invert color, 0 - else
                for i in inv:
                        rgb[i] = 1;
                        if rgb['r'] or rgb['g'] or rgb['b']: 
                                rgb['flag'] = 1     # need invert image
                        else:
                                rgb['flag'] = 0     # don't need invert image

                # convert images
                for i in jpg_list:
                        conv_im(i, grad, rgb)
                for j in png_list:
                        conv_im(j, grad, rgb)
	
#-------- MAIN ----------		

# parsing
parser = argparse.ArgumentParser(description = "Turn and invert pictures with formats .jpg or .png")
parser.add_argument("directory", default = "~", help = "Folder that contains pictures")
parser.add_argument("degrees", type = int, default = 0, help = "Number of degrees of rotation")
parser.add_argument("-i", "--invert", default = '', help = "Parametrs: r - red color, g - green color, b - black color")

args = parser.parse_args()	# parametrs

path = args.directory
grad = args.degrees
inv = args.invert.split(', ', maxsplit = 3)

conv_images(path, grad, inv)   # convert image
