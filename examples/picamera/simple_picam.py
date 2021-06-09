# import the necessary packages
from picam import PiCam
from time import sleep
import numpy as np
import cv2 as cv

res = (320, 240)
fps = 24

# initialize the camera
#camera = PiCam(res, fps, brightness=55, contrast=10)
#camera = PiCam(res, fps, awb_mode='shade')
camera = PiCam(res, fps, exposure_mode='night')

print('= eff =')
camera.effects()
print('= awb =')
camera.awbModes()
print('= exp =')
camera.exposureModes()

camera.videoCapture()

# allow the camera to warmup
sleep(2.0)

# capture frames from the camera
while True:
	frame = camera.current_frame
	cv.imshow('grid', frame)                           # show grid

	if cv.waitKey(1) & 0xFF == ord("q"):
		break

camera.release()
cv.destroyAllWindows()
