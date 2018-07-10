#!/usr/bin/python
# Import required libraries
import sys
import time
import RPi.GPIO as GPIO
 



def x_move(nsteps,direction):
	GPIO.setmode(GPIO.BOARD)
	 
	# Define GPIO signals to use
	# Physical pins 11,15,16,18
	# GPIO17,GPIO22,GPIO23,GPIO24
	StepPins = [33,31,29,32]
	# StepPins = [29,28,27,25]
	 
	# Set all pins as output
	for pin in StepPins:
	  # print("Setup pins")
	  GPIO.setup(pin,GPIO.OUT)
	  GPIO.output(pin, False)
	 
	# Define advanced sequence
	# as shown in manufacturers datasheet
	Seq = [[1,0,0,1],
	       [1,0,0,0],
	       [1,1,0,0],
	       [0,1,0,0],
	       [0,1,1,0],
	       [0,0,1,0],
	       [0,0,1,1],
	       [0,0,0,1]]
	        
	StepCount = len(Seq)
	StepDir = -1 # Set to 1 or 2 for clockwise
	            # Set to -1 or -2 for anti-clockwise
	 
	# Read wait time from command line
	# Initialise variables
	StepCounter = 0
	# Start main loop

	if direction is "right":
		StepDir = -1
	elif direction is "left":
		StepDir = 1
	else:
		StepDir = 1

	for i in range(0,nsteps):
	  time.sleep(0.01)
	  # print(StepCounter, end=' ')
	  # print(Seq[StepCounter])
	 
	  for pin in range(0, 4):
	    xpin = StepPins[pin]
	    if Seq[StepCounter][pin]!=0:
	      # print(" Enable GPIO %i" %(xpin))
	      GPIO.output(xpin, True)
	    else:
	      GPIO.output(xpin, False)  
	 
	  StepCounter += StepDir
	 
	  # If we reach the end of the sequence
	  # start again
	  if (StepCounter>=StepCount):
	    StepCounter = 0
	  if (StepCounter<0):
	    StepCounter = StepCount+StepDir


	for pin in StepPins:
	  # print("Setup pins")
	  # GPIO.setup(pin,GPIO.OUT)
	  GPIO.output(pin, False)


