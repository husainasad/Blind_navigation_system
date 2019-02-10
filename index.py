import pyttsx3
import RPi.GPIO as GPIO
import time
import SimpleMFRC522

def speech(str):
	print(str)
	engine = pyttsx3.init()
	engine.setProperty('rate', 120)
	engine.say(str)
	engine.runAndWait()

keyPressedBefore = False
totalSteps = 0
stepDuration = 1.25
startTime = 0
prevTime = 0
part1Steps = 0
part2Steps = 0
partOn = 0

def direct(num):
	global keyPressedBefore, totalSteps, stepDuration, startTime, prevTime, part1Steps, part2Steps, partOn
	if (num == 1):
		if (keyPressedBefore):
			totalSteps += round((time.time() - startTime) / stepDuration)
			startTime = time.time()
			if (partOn == 1):
				if (totalSteps < part1Steps):
					speech("You still have to take %d steps forward" % (part1Steps - totalSteps))
				elif (totalSteps == part1Steps):
					speech("Turn left and take 15 steps forward")
					partOn = 2
					totalSteps = 0
				elif(totalSteps > part1Steps):
					partOn = 2
					totalSteps = 0
			else:
				if (totalSteps < part2Steps):
					speech("You still have to take %d steps forward" % (part2Steps - totalSteps))
				elif (totalSteps >= part2Steps):
					speech("You have reached your destination")
					partOn = 2
					totalSteps = 0
		else:
			speech("You have opted to go to A, Take 20 steps forward, turn left and move 15 steps forward. Press 1 again for recalibrated instructions")
			keyPressedBefore = True
			partOn = 1
			startTime = time.time()
			totalSteps = 0
			part1Steps = 20
			part2Steps = 15

	elif (num == 2):
		if (keyPressedBefore):
			totalSteps += round((time.time() - startTime) / stepDuration)
			startTime = time.time()
			if (partOn == 1):
				if (totalSteps < part1Steps):
					speech("You still have to take %d steps forward" % (part1Steps - totalSteps))
				elif (totalSteps == part1Steps):
					speech("Turn left and take 25 steps forward")
					partOn = 2
					totalSteps = 0
				elif (totalSteps > part1Steps):
					partOn = 2
					totalSteps = 0	
			else:
				if (totalSteps < part2Steps):
					speech("You still have to take %d steps forward" % (part2Steps - totalSteps))
				elif (totalSteps >= part2Steps):
					speech("You have reached your destination")
					partOn = 2
					totalSteps = 0
		else:
			speech("You have opted to go to B, Turn right, move 15 steps forward then turn left and move 25 steps forward. Press 2 again for recalibrated instructions")
			keyPressedBefore = True
			partOn = 1
			startTime = time.time()
			totalSteps = 0
			part1Steps = 15
			part2Steps = 25

	elif (num == 3):
		if (keyPressedBefore):
			totalSteps += round((time.time() - startTime) / stepDuration)
			startTime = time.time()
			if (partOn == 1):
				if (totalSteps < part1Steps):
					speech("You still have to take %d steps forward" % (part1Steps - totalSteps))
				elif (totalSteps == part1Steps):
					speech("Turn right and turn 15 steps forward")
					partOn = 2
					totalSteps = 0
				elif(totalSteps > part1Steps):
					partOn = 2
					totalSteps = 0
			else:
				if (totalSteps < part2Steps):
					speech("You still have to take %d steps forward" % (part2Steps - totalSteps))
				elif (totalSteps >= part2Steps):
					speech("You have reached your destination")
					partOn = 2
					totalSteps = 0
		else:
			speech("You have opted to go to C, Turn around, move 10 steps forward then turn right and move 15 steps forward. Press 3 again for recalibrated instructions")
			keyPressedBefore = True
			partOn = 1
			startTime = time.time()
			totalSteps = 0
			part1Steps = 10
			part2Steps = 15

	elif (num == 4):
		if (keyPressedBefore):
			totalSteps += round((time.time() - startTime) / stepDuration)
			startTime = time.time()
			if (partOn == 1):
				if (totalSteps < part1Steps):
					speech("You still have to take %d steps forward" % (part1Steps - totalSteps))
				elif (totalSteps >= part1Steps):
					speech("You have reached your destination")
					partOn = 2
					totalSteps = 0
			else:
				if (totalSteps < part2Steps):
					speech("You still have to take %d steps forward" % (part2Steps - totalSteps))
				elif (totalSteps >= part2Steps):
					speech("You have reached your destination")
					partOn = 2
					totalSteps = 0
		else:
			speech("You have opted to go to D, Turn left, move 20 steps forward. Press 4 again for recalibrated instructions")
			keyPressedBefore = True
			partOn = 1
			startTime = time.time()
			totalSteps = 0
			part1Steps = 20
			part2Steps = 0

	else:
		speech("Invalid choice")

def speakMessages():
	speech("Authenticated")
	speech("Welcome to the Blind Accessibility Movement System. You will now be guided accordingly. Please pay attention to the navigation instructions.")
	speech("Press 1 to go to A")
	speech("Press 2 to go to B")
	speech("Press 3 to go to C")
	speech("Press 4 to go to D")

def authenticate():
	reader = SimpleMFRC522.SimpleMFRC522()
	try:
		while (True):
			id, text = reader.read()
			if (True):
				return id
	finally:
		GPIO.cleanup()
						
def main():
	print(authenticate())

	speakMessages()

	GPIO.setmode (GPIO.BOARD)

	MATRIX = [
		[1,2,3,'A'],
		[4,5,6,'B'],
		[7,8,9,'C'],
		['*',0,'#','D']
	]

	ROW = [7,11,13,15]
	COL = [31,33,35,37]

	for j in range(4):
		GPIO.setup(COL[j], GPIO.OUT)
		GPIO.output(COL[j], 1)

	for i in range (4):
		GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

	try:
		while(True):
			for j in range (4):
				GPIO.output(COL[j],0)
				for i in range(4):
					if GPIO.input (ROW[i]) == 0:
						direct(MATRIX[i][j])
						time.sleep(1)
						while (GPIO.input(ROW[i]) == 0):
							pass
				GPIO.output(COL[j],1)
	except KeyboardInterrupt:
			GPIO.cleanup()

main()