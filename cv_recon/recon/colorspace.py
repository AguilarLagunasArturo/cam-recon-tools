import cv2 as cv
import numpy as np
# cv.setUseOptimized(True)

class Colorspace:
	def __init__(self, hsv_settings = None):
		self.hsv_settings = hsv_settings

		if self.hsv_settings is not None:
			Colorspace.loadSettings(self, self.hsv_settings)
		else:
			self.lower = np.int32( [0, 0, 0] )
			self.upper = np.int32( [179, 255, 255] )

		self.im_mask = None
		self.im_cut = None
		self.im_edges = None

	def loadSettings(self, hsv_settings):
		try:
			with open(hsv_settings, 'r') as f:
				lines = f.read().split('\n')
				self.lower = np.int32( [value for value in lines[0].split(',')] )
				self.upper = np.int32( [value for value in lines[1].split(',')] )
		except Exception as e:
			print(e)
			exit()

	def getBoxes(self, im_base, im_hsv, min_area=20, scale=0.2):
		self.im_mask = cv.inRange(im_hsv, self.lower, self.upper)
		self.im_cut = cv.bitwise_and(im_base, im_base, mask=self.im_mask)
		self.im_edges = cv.Canny(self.im_mask, 100, 100)		# CAN ALSO BE A COLOR/MASK FRAME LESS IS BETTER


		boxes_within = []
		contours_within = []

		contours, _ = cv.findContours(self.im_edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)		# <- RESEARCH

		for c in contours:
			area = cv.contourArea(c)
			if area >= min_area:
				#cv.drawContours(output, c, -1, (255, 255, 255), 2)							# <- RESEARCH
				perimeter = cv.arcLength(c, True)
				points = cv.approxPolyDP(c, scale * perimeter, True)

				boxes_within.append( cv.boundingRect(points) )
				contours_within.append( c )

		return boxes_within, contours_within

if __name__ == '__main__':
	import sys
	from os import path
	sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
	import cv_tools

	colorspace = Colorspace()
	sample_mode =  True

	if len(sys.argv) == 1:
		cv.namedWindow('slides')
		cv.createTrackbar('hmin', 'slides',   0, 179, lambda x: x)
		cv.createTrackbar('hmax', 'slides', 179, 179, lambda x: x)
		cv.createTrackbar('smin', 'slides',   0, 255, lambda x: x)
		cv.createTrackbar('smax', 'slides', 255, 255, lambda x: x)
		cv.createTrackbar('vmin', 'slides',   0, 255, lambda x: x)
		cv.createTrackbar('vmax', 'slides', 255, 255, lambda x: x)
	elif len(sys.argv) == 2:
		sample_mode =  False
		try:
			colorspace.loadSettings(sys.argv[1])
		except Exception as e:
			print(e)
			exit()
	else:
		raise Exception('Wrong number of arguments')
		exit()

	cam = cv.VideoCapture(0)

	while True:
		if sample_mode:
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

		rec, frame = cam.read()

		if not rec:
			raise Exception('Cam is not recording')


		frame_blur = cv.GaussianBlur(frame, (9, 9), 150)											# BLUR SMOOTHES THE COLORSPACE
		frame_hsv = cv.cvtColor(frame_blur, cv.COLOR_BGR2HSV)

		boxes, _ = colorspace.getBoxes(frame, frame_hsv, 150)
		frame_out = cv_tools.drawOffset(frame.copy(), boxes)

		frame_grid = cv_tools.grid(frame, (2, 3),[
			frame, frame_hsv, frame_out,
			colorspace.im_cut, colorspace.im_mask, colorspace.im_edges
		])

		cv.imshow('grid', frame_grid)

		if cv.waitKey(1) & 0xFF == ord('q'):
			break

	cam.release()
	cv.destroyAllWindows()

	if sample_mode:
		with open('last.log', 'w') as f:
			f.write('{},{},{}\n{},{},{}'.format(
				colorspace.lower[0], colorspace.lower[1], colorspace.lower[2],
				colorspace.upper[0], colorspace.upper[1], colorspace.upper[2])
			)
