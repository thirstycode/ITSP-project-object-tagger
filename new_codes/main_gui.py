import RPi.GPIO as GPIO
from time import sleep
from tkinter import Frame, Label, Tk, BOTH, Text, Menu, INSERT, END, HORIZONTAL
from tkinter.ttk import Frame, Button, Style, Scale
import tkinter.filedialog
import tkinter.messagebox as mbox
import _thread
# from PIL import Image, ImageTk

# for dc motors
GPIO.setmode(GPIO.BOARD)
 




class aFrame(Frame):

	stepy = False
	stepx = False
	dc_running = False

	Motor1E = 22
	Motor1A = 16
	Motor1B = 18
	 
	Motor2E = 15
	Motor2B = 11
	Motor2A = 13

	w = None

	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.imageName = ""
		
		self.w = Scale(parent, from_=1, to=100, orient=HORIZONTAL)
		self.w.place(x=600, y=140)
		self.w.set(100)

		GPIO.setup(self.Motor1A,GPIO.OUT)
		GPIO.setup(self.Motor1B,GPIO.OUT)
		GPIO.setup(self.Motor1E,GPIO.OUT)
		 
		GPIO.setup(self.Motor2A,GPIO.OUT)
		GPIO.setup(self.Motor2B,GPIO.OUT)
		GPIO.setup(self.Motor2E,GPIO.OUT)

		self.initUI()

	def initUI(self):
		self.parent.title("DC Motor Control Box")
		self.style = Style().configure("TFrame", background="#333")
		# self.iconbitmap("icon.png")
		# self.style.theme_use("default")
		self.pack(fill=BOTH, expand=1)

		# quitButton = Button(self, text="Open File", command=self.onFilePicker)
		# quitButton.place(x=10, y=10)

		printButton = Button(self, text="Forward", command=self.forward_dc)
		printButton2 = Button(self, text="Left", command=self.left_dc)
		printButton3 = Button(self, text="Back", command=self.backwards_dc)
		printButton4 = Button(self, text="Right", command=self.right_dc)
		printButton5 = Button(self, text="Stop Motors", command=self.stop_dc)
		printButton6 = Button(self, text="Quit", command=self.quit)
		printButton7 = Button(self, text="Stop Stepper Y", command=self.stop_steppery)
		printButton8 = Button(self, text="Stepper up", command=self.thread_step_up)
		printButton9 = Button(self, text="Stepper Left", command=self.thread_step_left)
		printButton10 = Button(self, text="Stepper Down", command=self.thread_step_down)
		printButton11 = Button(self, text="Stepper Right", command=self.thread_step_right)
		printButton12 = Button(self, text="Stop Stepper X", command=self.stop_stepperx)
		printButton.place(x=200, y=40)
		printButton2.place(x=110, y=90)
		printButton3.place(x=200, y=90)
		printButton4.place(x=290, y=90)
		printButton5.place(x=210, y=200)
		printButton6.place(x=350, y=200)
		printButton7.place(x=400, y=85)
		printButton8.place(x=400, y=40)
		printButton9.place(x=500, y=90)
		printButton10.place(x=400, y=130)
		printButton11.place(x=710, y=90)
		printButton12.place(x=600, y=90)



		# self.thread_step_up()
		self.centerWindow()

	def set_speed(sefl,val):
		return round(-(0.09/100)*val + 0.1,3)

	def centerWindow(self):
		w = 1000
		h = 300

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw - w)/2
		y = (sh - h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


	def onDetect(self):
		pass

	def stop_dc(self):
		# print(self.w.get())
		# print(self.set_speed(self.w.get()))
		GPIO.output(self.Motor1E,False)
		GPIO.output(self.Motor2E,False)
		self.dc_running = False

	def forward_dc(self):
		if self.dc_running is True:
			self.stop_dc()
		else:
			GPIO.output(self.Motor1A,True)
			GPIO.output(self.Motor1B,False)
			GPIO.output(self.Motor1E,True)
			 
			GPIO.output(self.Motor2A,True)
			GPIO.output(self.Motor2B,False)
			GPIO.output(self.Motor2E,True)
			self.dc_running = True

	def backwards_dc(self):
		if self.dc_running is True:
			self.stop_dc()
		else:
			GPIO.output(self.Motor1A,False )
			GPIO.output(self.Motor1B,True)
			GPIO.output(self.Motor1E,True)
			 
			GPIO.output(self.Motor2A,False)
			GPIO.output(self.Motor2B,True)
			GPIO.output(self.Motor2E,True)
			self.dc_running = True

	def left_dc(self):
		if self.dc_running is True:
			self.stop_dc()
		else:
			GPIO.output(self.Motor1A,False )
			GPIO.output(self.Motor1B,True)
			GPIO.output(self.Motor1E,True)
			 
			GPIO.output(self.Motor2A,True)
			GPIO.output(self.Motor2B,False)
			GPIO.output(self.Motor2E,True)
			self.dc_running = True

	def right_dc(self):
		if self.dc_running is True:
			self.stop_dc()
		else:
			GPIO.output(self.Motor1A,True)
			GPIO.output(self.Motor1B,False)
			GPIO.output(self.Motor1E,True)

			GPIO.output(self.Motor2A,False)
			GPIO.output(self.Motor2B,True)
			GPIO.output(self.Motor2E,True)
			self.dc_running = True


	def stepper_up(self):
		# print(1)
		StepPins = [40,38,36,37]
		direction = 1

		for pin in StepPins:
			  #pass
			  GPIO.setup(pin,GPIO.OUT)
			  GPIO.output(pin, False)

		Seq = [[1,0,0,1],
		       [1,0,0,0],
		       [1,1,0,0],
		       [0,1,0,0],
		       [0,1,1,0],
		       [0,0,1,0],
		       [0,0,1,1],
		       [0,0,0,1]]
		        
		StepCount = len(Seq)

		StepCounter = 0

		while self.stepy is True:
		  sleep(self.set_speed(self.w.get()))
		  # print StepCounter,
		  # print Seq[StepCounter]
		 
		  for pin in range(0, 4):
		    xpin = StepPins[pin]
		    if Seq[StepCounter][pin]!=0:
		      # print " Enable GPIO %i" %(xpin)
		      GPIO.output(xpin, True)
		    else:
		      GPIO.output(xpin, False)
		 
		  StepCounter += direction
		 
		  if (StepCounter>=StepCount):
		    StepCounter = 0
		  if (StepCounter<0):
		    StepCounter = StepCount+direction
		
		for pin in StepPins:
		  # print "Setup pins"
		  GPIO.setup(pin,GPIO.OUT)
		  GPIO.output(pin, False)


	def stepper_down(self):
		StepPins = [40,38,36,37]
		direction = -1

		for pin in StepPins:
			  #pass
			  GPIO.setup(pin,GPIO.OUT)
			  GPIO.output(pin, False)

		Seq = [[1,0,0,1],
		       [1,0,0,0],
		       [1,1,0,0],
		       [0,1,0,0],
		       [0,1,1,0],
		       [0,0,1,0],
		       [0,0,1,1],
		       [0,0,0,1]]
		        
		StepCount = len(Seq)

		StepCounter = 0

		while self.stepy is True:
		  sleep(self.set_speed(self.w.get()))
		  # print StepCounter,
		  # print Seq[StepCounter]
		 
		  for pin in range(0, 4):
		    xpin = StepPins[pin]
		    if Seq[StepCounter][pin]!=0:
		      # print " Enable GPIO %i" %(xpin)
		      GPIO.output(xpin, True)
		    else:
		      GPIO.output(xpin, False)
		 
		  StepCounter += direction
		 
		  if (StepCounter>=StepCount):
		    StepCounter = 0
		  if (StepCounter<0):
		    StepCounter = StepCount+direction
		
		for pin in StepPins:
		  # print "Setup pins"
		  GPIO.setup(pin,GPIO.OUT)
		  GPIO.output(pin, False)

	def stepper_left(self):
		# print(1)
		StepPins = [33,31,29,32]
		direction = 1

		for pin in StepPins:
			  #pass
			  GPIO.setup(pin,GPIO.OUT)
			  GPIO.output(pin, False)

		Seq = [[1,0,0,1],
		       [1,0,0,0],
		       [1,1,0,0],
		       [0,1,0,0],
		       [0,1,1,0],
		       [0,0,1,0],
		       [0,0,1,1],
		       [0,0,0,1]]
		        
		StepCount = len(Seq)

		StepCounter = 0

		while self.stepx is True:
		  sleep(self.set_speed(self.w.get()))
		  # print StepCounter,
		  # print Seq[StepCounter]
		 
		  for pin in range(0, 4):
		    xpin = StepPins[pin]
		    if Seq[StepCounter][pin]!=0:
		      # print " Enable GPIO %i" %(xpin)
		      GPIO.output(xpin, True)
		    else:
		      GPIO.output(xpin, False)
		 
		  StepCounter += direction
		 
		  if (StepCounter>=StepCount):
		    StepCounter = 0
		  if (StepCounter<0):
		    StepCounter = StepCount+direction
		
		for pin in StepPins:
		  # print "Setup pins"
		  GPIO.setup(pin,GPIO.OUT)
		  GPIO.output(pin, False)


	def stepper_right(self):
		StepPins = [33,31,29,32]
		direction = -1

		for pin in StepPins:
			  #pass
			  GPIO.setup(pin,GPIO.OUT)
			  GPIO.output(pin, False)

		Seq = [[1,0,0,1],
		       [1,0,0,0],
		       [1,1,0,0],
		       [0,1,0,0],
		       [0,1,1,0],
		       [0,0,1,0],
		       [0,0,1,1],
		       [0,0,0,1]]
		        
		StepCount = len(Seq)

		StepCounter = 0

		while self.stepx is True:
		  sleep(self.set_speed(self.w.get()))
		  # print StepCounter,
		  # print Seq[StepCounter]
		 
		  for pin in range(0, 4):
		    xpin = StepPins[pin]
		    if Seq[StepCounter][pin]!=0:
		      # print " Enable GPIO %i" %(xpin)
		      GPIO.output(xpin, True)
		    else:
		      GPIO.output(xpin, False)
		 
		  StepCounter += direction
		 
		  if (StepCounter>=StepCount):
		    StepCounter = 0
		  if (StepCounter<0):
		    StepCounter = StepCount+direction
		
		for pin in StepPins:
		  # print "Setup pins"
		  GPIO.setup(pin,GPIO.OUT)
		  GPIO.output(pin, False)


	def stop_steppery(self):
		self.stepy = False

	def stop_stepperx(self):
		self.stepx = False

	def thread_step_up(self):
		self.stepy = True
		_thread.start_new_thread(self.stepper_up,())

	def thread_step_down(self):
		self.stepy = True
		_thread.start_new_thread(self.stepper_down,())

	def thread_step_left(self):
		self.stepx = True
		_thread.start_new_thread(self.stepper_left,())

	def thread_step_right(self):
		self.stepx = True
		_thread.start_new_thread(self.stepper_right,())

if __name__ == '__main__':
    root = Tk()
    # root.iconbitmap(r"1.ico")
    app = aFrame(root)
    root.mainloop()
