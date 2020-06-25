from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import RPi.GPIO as GPIO
import time
import os
from os import listdir
from os.path import isfile, join
import subprocess

import ST7789

global imagepath 

current_record = 0
imagepath= '/home/pi/scripts/images'
mypath = '/home/pi/scripts/images'
roms = '/home/pi/scripts/roms'
list_of_images = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(list_of_images)
number_of_files = len(list_of_images)

for i in list_of_images: 
    print(i) 


MESSAGE = "ZX Spectrum Loader"

# Create ST7789 LCD display class.
disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CSB_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000
)

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height


# Set up the basics for buttons. The buttons on Pirate Audio are connected to pins 5, 6, 16 and 20
BUTTONS = [5, 6, 16, 20]

# These correspond to buttons A, B, X and Y respectively
LABELS = ['A', 'B', 'X', 'Y']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Increment and decrement game
def increment():
	global current_record
	global number_of_files

	if (current_record+1) < number_of_files:
		current_record = current_record+1

def decrement():
	global current_record
	global number_of_files

	if (current_record-1) >= 0:
		current_record = current_record-1

def play_game():
	global current_record
	global list_of_images
	file_name = list_of_images[current_record]
	rename_file = os.path.splitext(file_name)[0]+'.tzx'
	full_path = roms + '/' + rename_file	
	print(full_path)
	#print os.path.splitext('/home/user/somefile.txt')[0]+'.jpg'
	subprocess.Popen(r'/home/pi/scripts//playcdt.sh ' + full_path, shell=True)


# Display correct piture

def select_game(file_id,list_of_images):

	file_name = list_of_images[file_id]
	full_path = imagepath + '/' + file_name	
	#print (file_name)
	rgba_image = Image.open(full_path)
	newsize = (240, 240) 
	rgba_image = rgba_image.resize(newsize)
	disp.display(rgba_image)

# Set up the button handler
def handle_button(pin):
	label = LABELS[BUTTONS.index(pin)]
	print("Button press detected on pin: {} label: {}".format(pin, label))

	if label=='A':
		#Go to previous item
		decrement()

	if label=='X':
		#Play file
		play_game()
		#subprocess.Popen(r'./playcdt.sh games/manicminer.tzx', shell=True)
		

	if label=='B':
		#Go to next item
		increment()

	if label=='Y':
		#Pause / Unpause VLC
		os.system('dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2   org.mpris.MediaPlayer2.Player.PlayPause')

		


for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=400)

while True:

	select_game(current_record, list_of_images)
