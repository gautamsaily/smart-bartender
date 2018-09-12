import time
import threading
			#rum	vodka	tequila	oj		gin		coke	mmix
drinkmenu = [[0,	0,		20,		0,		0,		0,		60],	#margarita
			 [20,	0,		0,		0,		0,		60,		0],		#rum n coke
			 [7,	7,		7,		7,		7,		40,		0],		#long island
			 [0,	20,		0,		60,		0,		0,		0],		#screw driver
			 [0,	0,		20,		60,		0,		0,		0],		#tequila sunrise
			 [0,	0,		0,		60,		20,		0,		0]]		#gin n juice

pump_config =	{
	1	:	17, 	#"rum",
	2	:	18, 	#"vodka",
	3	:	19,		#"tequila",
	4	:	20,		#"oj",
	5	:	21,		#"gin",
	6	:	22,		#"coke",
	7	:	23,		#"mmix"
}  #pump	pin

drink_index =	{
	"margarita"			:	0,
	"rum n coke"		:	1,
	"long island"		:	2,
	"screw driver"		:	3,
	"tequila sunrise"	:	4,
	"gin n juice"		:	5
}

def turnOn(pin, seconds):
	print "Pin %d seconds %d\n" % (pin, seconds)
	time.sleep(seconds)

def gautam_function(drink):
	print "Hello World"

	menu_idx = drink_index.get(drink)
	pumpThreads = []
	for pump in range(0, 6):
		seconds = drinkmenu[menu_idx][pump]
		if (0 != seconds):
			pin = pump_config.get(pump + 1)
			pump_t = threading.Thread(target=turnOn, args=(pin,seconds, ))
			pumpThreads.append(pump_t)
	for thread in pumpThreads:
		thread.start()
	for thread in pumpThreads:
		thread.join()
	print "done"

def main():
	gautam_function("long island")

main()