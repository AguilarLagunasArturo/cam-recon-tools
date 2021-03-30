import sys
import cv2 as cv
import numpy as np
from tools.cv_tools import grid, draw_boxes

cv.setUseOptimized(True)

sample_mode = True

if len(sys.argv) == 1:
	cv.namedWindow('slides')
	cv.createTrackbar('hmin', 'slides',   0, 179, lambda x: x)
	cv.createTrackbar('hmax', 'slides', 179, 179, lambda x: x)
	cv.createTrackbar('smin', 'slides',   0, 255, lambda x: x)
	cv.createTrackbar('smax', 'slides', 255, 255, lambda x: x)
	cv.createTrackbar('vmin', 'slides',   0, 255, lambda x: x)
	cv.createTrackbar('vmax', 'slides', 255, 255, lambda x: x)
	cv.createTrackbar('canny1', 'slides', 50, 500, lambda x: x)
	cv.createTrackbar('canny2', 'slides', 50, 500, lambda x: x)

elif len(sys.argv) == 2:
	try:
		with open(sys.argv[1], 'r') as f:
			lines = f.read().split('\n')
			lower = np.array( [int(value) for value in lines[0].split(',')] )
			upper = np.array( [int(value) for value in lines[1].split(',')] )
			sample_mode =  False
	except Exception as e:
		print(e)
		exit()
else:
	raise Exception('Wrong number of arguments')
	exit()
cam = cv.VideoCapture(0)
canny_settings = [144, 57]
while True:
	if sample_mode:
		lower = np.array([
			cv.getTrackbarPos('hmin', 'slides'),
			cv.getTrackbarPos('smin', 'slides'),
			cv.getTrackbarPos('vmin', 'slides')
		])
		upper = np.array([
			cv.getTrackbarPos('hmax', 'slides'),
			cv.getTrackbarPos('smax', 'slides'),
			cv.getTrackbarPos('vmax', 'slides')
		])
		canny_settings = [
			cv.getTrackbarPos('canny1', 'slides'),
			cv.getTrackbarPos('canny2', 'slides')
		]

	rec, frame = cam.read()
	frame_blur = cv.GaussianBlur(frame, (9, 9), 150)				# BLUR SMOOTHES THE COLORSPACE
	frame_hsv = cv.cvtColor(frame_blur, cv.COLOR_BGR2HSV)
	frame_mask = cv.inRange(frame_hsv, lower, upper)
	frame_cut = cv.bitwise_and(frame, frame, mask=frame_mask)
	#frame_gray = cv.cvtColor(frame_cut, cv.COLOR_BGR2GRAY)
	frame_edges = cv.Canny(frame_mask, canny_settings[0], canny_settings[1])					# CAN ALSO BE A COLOR/MASK FRAME LESS IS BETTER
	frame_output = draw_boxes(frame_edges, frame.copy(), min_area=500)
	cv.line(
		frame_output,
		(0, int(frame.shape[0]/2)),
		(frame.shape[1], int(frame.shape[0]/2)),
		(0, 255, 0), 2
	)
	cv.line(
		frame_output,
		(int(frame.shape[1]/2), 0),
		(int(frame.shape[1]/2), frame.shape[0] ),
		(0, 255, 0), 2
	)

	frame_grid = grid(frame, (2,3), [frame, frame_output, frame_hsv, frame_cut, frame_mask, frame_edges])
	cv.imshow('grid', frame_grid)

	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cam.release()
cv.destroyAllWindows()

if sample_mode:
	with open('logs/last.log', 'w') as f:
		f.write('{},{},{}\n{},{},{}'.format(lower[0], lower[1], lower[2], upper[0], upper[1], upper[2]))
