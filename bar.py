import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import threading
#import global
#----------- Global Variable ------------#
press_count_right=0

input_string=["Margarita",
								"Whiskey N Water",
								"Rum N Coke",
								"Long Island",
								"Screw Driver",
								"Tequila Sunrise",
								"Gin N Juice",
								"P1",
								"P2",
								"P3",
								"P4",
								"P5",
								"P6",
								"Clean Right",
								"Clean Left",
								"Clean All"]
								#rum		vodka	tequila	oj			gin			coke		mmix
drinkmenu =	[[0,			0,			20,			0,			0,			0,			60],	#margarita
								[0,			0,			0,			0,			20,			40,			0],		#whiskeywater
								[20,		0,			0,			0,			0,			60,			0],		#rum n coke
								[7,			7,			7,			7,			7,			40,			0],		#long island
								[0,			20,			0,			60,			0,			0,			0],		#screw driver
								[0,			0,			20,			60,			0,			0,			0],		#tequila sunrise
								[0,			0,			0,			60,			20,			0,			0],	   #gin n juice
								[20,		0,			0,			0,			0,			0,			0],	   #gin n juice
								[0,			20,			0,			0,			0,			0,			0],	   #gin n juice
								[0,			0,			20,			0,			0,			0,			0],	   #gin n juice
								[0,			0,			0,			20,			0,			0,			0],	   #gin n juice
								[0,			0,			0,			0,			20,			0,			0],	   #gin n juice
								[0,			0,			0,			0,			0,			20,			0],	   #gin n juice
								[20,		20,			20,			0,			0,			0,			0],		#clean left
								[0,			0,			0,			20,			20,			20,			0],	  	#clean right
								[20,		20,			20,			20,			20,			20,			0]]		#clean left

pump_config =	{
	1	:	23, 	#"rum",
	2	:	24, 	#"vodka",
	3	:	25,		#"tequila",
	4	:	12,		#"oj",
	5	:	16,		#"gin",
	6	:	20,		#"coke",
	7	:	21,		#"mmix"
}  #pump	pin

drink_index =	{
	"Margarita"					:	0,
	"Whiskey N Water"	:	1,
	"Rum N Coke"			:	2,
	"Long Island"				:	3,
	"Screw Driver"			:	4,
	"Tequila Sunrise"		:	5,
	"Gin N Juice"				:	6,
	"P1"									:	7,
	"P2"									:	8,
	"P3"									:	9,
	"P4"									:	10,
	"P5"									:	11,
	"P6"									:	12,
	"Clean Left"					:	13,
	"Clean Right"				:	14,
	"Clean All"					:	15
}

#-----------LCD Init Start---------------#
# Raspberry Pi pin configuration:
print 'Initializing Display'
lcd_rs        = 26  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 11
lcd_backlight = 10
		
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2
		
# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
lcd.clear()
lcd.message('Bartender\nAwake!')
print 'Initilization Display Done'
#-----------LCD Init Finish---------------#

def setup_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(23, GPIO.HIGH)
    GPIO.output(24, GPIO.HIGH)
    GPIO.output(25, GPIO.HIGH)
    GPIO.output(12, GPIO.HIGH)
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#button left
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#button right
	
def LCD_Scroll():
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                               lcd_columns, lcd_rows, lcd_backlight)
    lcd.clear()
    message = 'Scroll'
    lcd.message(message)
    for i in range(lcd_columns-len(message)):
        time.sleep(0.5)
        lcd.move_right()
    for i in range(lcd_columns-len(message)):
        time.sleep(0.5)
        lcd.move_left()
    lcd.clear()

def turnOn(pin, seconds):
    seconds=seconds
    print "Pin %d seconds %d\n" % (pin, seconds)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(seconds)
    GPIO.output(pin, GPIO.HIGH)

def make_drink_function(drink):
    menu_idx = drink_index.get(drink)
    print "\nMaking ", drink
    pumpThreads = []
    for pump in range(0, 7):
	seconds = drinkmenu[menu_idx][pump]
	if (0 != seconds):
	    pin = pump_config.get(pump + 1)
	    pump_t = threading.Thread(target=turnOn, args=(pin,seconds, ))
	    pumpThreads.append(pump_t)
    for thread in pumpThreads:
	thread.start()
    for thread in pumpThreads:
	thread.join()
	
def main():	
	button_pressed_right=False
	button_pressed_left=False
	press_count_right=0
	press_count_left=0
	try:
		while (1):
			input_state_right_button = GPIO.input(4)
			input_state_left_button = GPIO.input(17)
			if input_state_right_button == False:
				print('Right Button Pressed')
				time.sleep(0.3)
				button_pressed_right=True
				press_count_right+=1
				if press_count_right==len(input_string)+1:
					press_count_right=1
			if input_state_left_button == False:
				print ('Left Button Pressed')
				time.sleep(0.3)
				button_pressed_left=True
				press_count_left+=1
	
			if button_pressed_left==True:
				button_pressed_left=False
				lcd.clear()
				lcd.message('Making Drink\n' + input_string[press_count_right-1])
				#Here is the routine for drink making
				make_drink_function(input_string[press_count_right-1])
				print 'sleep done'
				time.sleep(0.3)
				lcd.clear()
				time.sleep(0.3)
				lcd.message('Your Drink \nIs Ready')
				time.sleep(5)
				button_pressed_right=True
	
			if button_pressed_right==True:
				button_pressed_right=False
				lcd.clear()				
				lcd.message(input_string[press_count_right-1])

	except KeyboardInterrupt:
		print 'Quit'
		lcd.clear()
		GPIO.cleanup()

setup_GPIO()
main()
