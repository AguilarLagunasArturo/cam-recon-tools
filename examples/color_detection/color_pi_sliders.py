# import the necessary packages
from cv_recon import Colorspace
from cv_recon import cv_tools
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from time import sleep
import numpy as np
import cv2 as cv

res = (320, 240)

# initialize the camera
camera = PiCamera()
# camera.image_effect = 'none'
camera.brightness = 55
camera.contrast = 10
camera.awb_mode = 'tungsten'
# camera.exposure_mode = 'off'
camera.resolution = res
camera.framerate = 32
# grab a reference to the raw camera capture
rawCapture = PiRGBArray(camera, size=res)
# get frame stream from the camera
stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)

frame = None

colorspace = Colorspace('examples/color_detection/logs/blue2.log')

cv.namedWindow('slides')
cv.createTrackbar('hmin', 'slides',   0, 179, lambda x: x)
cv.createTrackbar('hmax', 'slides', 179, 179, lambda x: x)
cv.createTrackbar('smin', 'slides',   0, 255, lambda x: x)
cv.createTrackbar('smax', 'slides', 255, 255, lambda x: x)
cv.createTrackbar('vmin', 'slides',   0, 255, lambda x: x)
cv.createTrackbar('vmax', 'slides', 255, 255, lambda x: x)

def update():
	global stream
	for f in stream:
		global frame
		frame = f.array
		rawCapture.truncate(0)

t = Thread(target=update, args=())
t.daemon = True
t.start()

# allow the camera to warmup
sleep(2.0)

# capture frames from the camera
while True:
	colorspace.lower = np.array([
		cv.getTrackbarPos('hmin', 'slides'),
		cv.getTrackbarPos('smin', 'slides'),
		cv.getTrackbarPos('vmin', 'slides')
	])
	colorspace.upper = np.array([
		cv.getTrackbarPos('hmax', 'slides'),
		cv.getTrackbarPos('smax', 'slides'),
		cv.getTrackbarPos('vmax', 'slides')
	])

	#cv2.imshow("Frame", frame)
	frame_blur = cv.GaussianBlur(frame, (9, 9), 150)                # smoothes the noise
	frame_hsv = cv.cvtColor(frame_blur, cv.COLOR_BGR2HSV)   # convert BGR to HSV

	boxes = colorspace.getMaskBoxes(frame, frame_hsv, 150)  # get boxes (x, y, w, h)

	offsets = cv_tools.getBoxesOffset(frame, boxes)                 # get boxes offset from the center of the frame
	for i, offset in enumerate(offsets):
		print(i, offset)                                    # print offset (x_off, y_off)

	frame_out = cv_tools.drawBoxes(frame.copy(), boxes)     # draw boxe
	frame_out = cv_tools.drawBoxesPos(frame_out, boxes)     # draw offsets

	frame_grid = cv_tools.grid(frame, (2, 3),[              # generate grid
		frame_hsv, frame_out, colorspace.im_contours,
		colorspace.im_cut, colorspace.im_mask, colorspace.im_edges])

	cv.imshow('grid', frame_grid)                           # show grid

	if cv.waitKey(1) & 0xFF == ord("q"):
		break

stream.close()
rawCapture.close()
camera.close()

cv.destroyAllWindows()
