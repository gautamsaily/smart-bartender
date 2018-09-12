import RPi.GPIO as GPIO
import time
import threading

drinks = ["margarita", "rum n coke", "long island", "screw driver", "tequila sunrise", "gin n juice"]
			#rum	vodka	tequila	oj		gin		coke	mmix
drinkmenu =  [[0,	0,		20,		0,		0,		0,		60],	#margarita
			 [20,	0,		0,		0,		0,		60,		0],		#rum n coke
			 [7,	7,		7,		7,		7,		40,		0],		#long island
			 [0,	20,		0,		60,		0,		0,		0],		#screw driver
			 [0,	0,		20,		60,		0,		0,		0],		#tequila sunrise
			 [0,	0,		0,		60,		20,		0,		0]]		#gin n juice

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
	"margarita"			:	0,
	"rum n coke"		:	1,
	"long island"		:	2,
	"screw driver"		:	3,
	"tequila sunrise"	:	4,
	"gin n juice"		:	5
}

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

def turnOn(pin, seconds):
	print "Pin %d seconds %d\n" % (pin, seconds)
	GPIO.output(pin, GPIO.LOW)
	time.sleep(seconds)
	GPIO.output(pin, GPIO.HIGH)

def gautam_function(drink):
	menu_idx = drink_index.get(drink)
	pumpThreads = []
	for pump in range(0, 7):
		print pump
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
	setup_GPIO()
	for drink in drinks:
		print drink + " starting\n"
		gautam_function(drink)
		print drink + " done\n"
		time.sleep(0.5)

main()