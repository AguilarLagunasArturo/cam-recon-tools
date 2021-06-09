# import the necessary packages
from cv_recon.picam import PiCam
from cv_recon import Colorspace
from cv_recon import cv_tools
from time import sleep
import numpy as np
import cv2 as cv

res = (320, 240)
fps = 24

# initialize the camera
camera = PiCam(res, fps)

camera.effects()
camera.awb_modes()
camera.exposure_modes()

camera.video_capture()
colorspace = Colorspace('examples/color_detection/logs/blue2.log')

# allow the camera to warmup
sleep(2.0)

# capture frames from the camera
while True:
	frame = camera.current_frame
	print(type(frame))
	frame_blur = cv.GaussianBlur(frame, (9, 9), 150)                # smoothes the noise
	frame_hsv = cv.cvtColor(frame_blur, cv.COLOR_BGR2HSV)   	# convert BGR to HSV

	boxes = colorspace.getMaskBoxes(frame, frame_hsv, 150)  # get boxes (x, y, w, h)

	offsets = cv_tools.getBoxesOffset(frame, boxes)                 # get boxes offset from the center of the frame
	#for i, offset in enumerate(offsets):
	#	print(i, offset)                                    # print offset (x_off, y_off)

	frame_out = cv_tools.drawBoxes(frame.copy(), boxes)     # draw boxe
	frame_out = cv_tools.drawBoxesPos(frame_out, boxes)     # draw offsets

	frame_grid = cv_tools.grid(frame, (2, 3),[              # generate grid
		frame_hsv, frame_out, colorspace.im_contours,
		colorspace.im_cut, colorspace.im_mask, colorspace.im_edges], 1)

	cv.imshow('grid', frame_grid)                           # show grid

	if cv.waitKey(1) & 0xFF == ord("q"):
		break

camera.release()
cv.destroyAllWindows()
