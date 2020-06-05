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
imagepath= '/home/pi/scripts/images'
mypath = '/home/pi/scripts/images'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)
number_of_files = len(onlyfiles)

for i in onlyfiles: 
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


img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))

draw = ImageDraw.Draw(img)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)

size_x, size_y = draw.textsize(MESSAGE, font)

text_x = disp.width
text_y = (80 - size_y) // 2

t_start = time.time()

# Set up the basics for buttons. The buttons on Pirate Audio are connected to pins 5, 6, 16 and 20
BUTTONS = [5, 6, 16, 20]

# These correspond to buttons A, B, X and Y respectively
LABELS = ['A', 'B', 'X', 'Y']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Display correct piture

def select_game(file_id,list_of_images):
	#print(list_of_images)
	#print(file_id)

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
		#os.system("./playcdt.sh games/manicminer.tzx")
		#subprocess.Popen(r'./playcdt.sh games/manicminer.tzx',shell = True)
		subprocess.Popen(r'./playcdt.sh games/manicminer.tzx', shell=True)

	if label=='X':
		# button X - show the colour image, and pause for a second
		screen.display(image[0])
		draw_grid(2)
		screen.display(image[2])
		time.sleep(60)
		screen.display(image[3])

	if label=='B':
		# button B - show the logo image, and pause for a second
		#screen.display(image[1])
		#time.sleep(2)
		#screen.display(image[3])
		os.system('dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2   org.mpris.MediaPlayer2.Player.PlayPause')

	if label=='Y':
		# button Y - show the blank image, and exit
		screen.display(image[0])
		GPIO.cleanup()
		exit()

for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=400)

while True:

	select_game(0, onlyfiles)
	#rgba_image = Image.open('manicminer.png')
	#newsize = (240, 240) 
	#rgba_image = rgba_image.resize(newsize)
	#disp.display(rgba_image)
