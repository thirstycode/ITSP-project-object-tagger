import cv2
import time
import numpy as np
from supporting_files import stitch
from supporting_files import output


# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
# import cv2
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
#camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
 
# allow the camera to warmup
time.sleep(0.1)
 

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

# vid = cv2.VideoCapture(0)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
    # check , frame = vid.read()
    cv2.imshow("Click 'c' To Give Coordinates! 'q' to Close",image)
    if initial_frame is 1:
        # first frame set
        if frame1_count is 1:
            frame1 = image
            frame_paro = image
            frame1_count = 0

        frame_paro = stitch.stitch(frame_paro,image)
        if frame_paro.shape[1] - 25 < frame1.shape[1] + xcor < frame_paro.shape[1] + 25 :
            print("no output , target is in range ")
        else :
            output.output()



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
