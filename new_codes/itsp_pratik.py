import cv2
import time
import numpy as np
from supporting_files.outputx import x_move
from supporting_files.outputy import y_move
import _thread
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from math import sqrt,cos,sin,atan

rng = 50
hori_fov = 53.50
ver_fov = 41.41
x_error = 22*3
y_error = 0
r_change = 1.25
y_change = 1.32

xcor,ycor = -1,-1
initial_frame = 0
frame1_count = 0
# mouse callback function
def fetch_coord(event,x,y,flags,param):
    global xcor,ycor,initial_frame,frame1_count
    xcor,ycor = x,y

img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow("Click 'c' To Give Coordinates! 'q' to Close")
cv2.setMouseCallback("Click 'c' To Give Coordinates! 'q' to Close",fetch_coord)

vid = cv2.VideoCapture(0)

movement_x = False

 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (960, 720)
#camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(960, 720))
 
# allow the camera to warmup
time.sleep(0.1)
 

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	frame = frame.array
	cv2.imshow("Click 'c' To Give Coordinates! 'q' to Close",frame)
    # cv2.imshow("Click 'c' To Give Coordinates! 'q' to Close",frame)
	if initial_frame is 1:
        # first frame set
		if frame1_count is 1:
			frame1 = frame
			frame1_count = 0

		frame_x = frame1.shape[1]
		frame_y = frame1.shape[0]

		x_origin = frame_x/2 - x_error
		y_origin = frame_y/2
        # if frame_paro.shape[1] - 50 < frame1.shape[1] + xcor < frame_paro.shape[1] + 50 :
        #     print("no output , target is in range ")
        # else :
        #     output.output()
        # xcor += x_error
		if xcor > x_origin:
			print("move_left")
			directionx = 'right'
		elif xcor < x_origin:
			print("move_right")
			directionx = 'left'
		else:
			print("Target is in range in x Coordinates")

		if ycor > y_origin:
			print("move_down")
			directiony = 'down'
		elif ycor < y_origin:
			print("move_up")
			directiony = 'up'
		else:
			print("Target is in range in y Coordinates")

		radius = sqrt((abs(x_origin - xcor))**2 + (abs(y_origin - ycor))**2 )
		slope = (y_origin - ycor)/(x_origin - xcor)
		radius = radius*r_change
		diff_x = radius*cos(atan(slope))
		diff_y = radius*sin(atan(slope))/r_change*y_change

		# diff_x = abs(xcor - x_origin)
		nsteps_x = abs(int((hori_fov*diff_x*1000)/(frame_x*90)))
		# if directionx is 'left':
		# 	nsteps_x_error = -1*int((hori_fov*x_error*1000)/(frame_x*90))
		# elif directionx is 'right':
		# 	nsteps_x_error = 1*int((hori_fov*x_error*1000)/(frame_x*90))
		# x_move(nsteps_x,directionx)
		_thread.start_new_thread(x_move,(nsteps_x ,directionx,))
		print("nsteps_x = " + str(nsteps_x) + " directionx = " + directionx)
		print("x move complete")
		# diff_y = abs(ycor - y_origin)
		nsteps_y = abs(int((ver_fov*diff_y*1000)/(frame_y*90)))
		# y_move(nsteps_y,directiony)
		_thread.start_new_thread(y_move,(nsteps_y,directiony,))
		print("nsteps_y = " + str(nsteps_y) + " directiony = " + directiony)
		print("y move complete")
		initial_frame = 0


	rawCapture.truncate(0)
	key = cv2.waitKey(1)
	if key == ord('q'):
	    break
	elif key == ord('c'):
	    print (xcor,ycor)
	    initial_frame = 1
	    frame1_count = 1
vid.release()
cv2.destroyAllWindows()
