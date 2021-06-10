import cv2 as cv
import numpy as np

class Colorspace:
	def __init__(self, hsv_settings=None):
		if hsv_settings is None:
			self.lower = np.int32( [0, 0, 0] )
			self.upper = np.int32( [179, 255, 255] )
		elif type(hsv_settings) is list and np.int32(hsv_settings).shape == (2,3):
			self.lower = np.int32( [hsv_settings[0]] )
			self.upper = np.int32( [hsv_settings[1]] )
		else:
			Colorspace.loadSettings(self, hsv_settings)
		self.im_mask = None
		self.im_cut = None
		self.im_edges = None
		self.im_contours = None

	def loadSettings(self, settings):
		try:
			with open(settings, 'r') as f:
				lines = f.read().split('\n')
				self.lower = np.int32( [value for value in lines[0].split(',')] )
				self.upper = np.int32( [value for value in lines[1].split(',')] )
		except Exception as e:
			print(e)
			exit()

	def dumpSettings(self, output='last.log'):
		with open(output, 'w') as f:
			f.write('{},{},{}\n{},{},{}'.format(
				self.lower[0], self.lower[1], self.lower[2],
				self.upper[0], self.upper[1], self.upper[2])
			)

	@staticmethod
	def createSliders():
		cv.namedWindow('sliders')
		cv.createTrackbar('hmin', 'sliders',   0, 179, lambda x: x)
		cv.createTrackbar('hmax', 'sliders', 179, 179, lambda x: x)
		cv.createTrackbar('smin', 'sliders',   0, 255, lambda x: x)
		cv.createTrackbar('smax', 'sliders', 255, 255, lambda x: x)
		cv.createTrackbar('vmin', 'sliders',   0, 255, lambda x: x)
		cv.createTrackbar('vmax', 'sliders', 255, 255, lambda x: x)

	def updateHSV(self):
		self.lower = np.array([
			cv.getTrackbarPos('hmin', 'sliders'),
			cv.getTrackbarPos('smin', 'sliders'),
			cv.getTrackbarPos('vmin', 'sliders')
		])
		self.upper = np.array([
			cv.getTrackbarPos('hmax', 'sliders'),
			cv.getTrackbarPos('smax', 'sliders'),
			cv.getTrackbarPos('vmax', 'sliders')
		])

	def getMaskBoxes(self, im_base, im_hsv, min_area=20, scale=0.1):
		self.im_mask = cv.inRange(im_hsv, self.lower, self.upper)
		self.im_cut = cv.bitwise_and(im_base, im_base, mask=self.im_mask)
		self.im_edges = cv.Canny(self.im_mask, 100, 100)
		self.im_contours = im_base.copy()

		boxes_within = []
		contours, _ = cv.findContours(self.im_edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)	# <- DO RESEARCH

		for c in contours:
			area = cv.contourArea(c)
			if area >= min_area:
				perimeter = cv.arcLength( c, True )
				points = cv.approxPolyDP( c, scale * perimeter, True )
				boxes_within.append(cv.boundingRect(points))
				cv.drawContours(self.im_contours, c, -1, (255, 255, 255), 2)					# <- DO RESEARCH

		return boxes_within

	def getMaskBoxesArea(self, im_base, im_hsv, min_area=20, scale=0.1):
		self.im_mask = cv.inRange(im_hsv, self.lower, self.upper)
		self.im_cut = cv.bitwise_and(im_base, im_base, mask=self.im_mask)
		self.im_edges = cv.Canny(self.im_mask, 100, 100)
		self.im_contours = im_base.copy()

		boxes_within = []
		area_within = []
		contours, _ = cv.findContours(self.im_edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)	# <- DO RESEARCH

		for c in contours:
			area = cv.contourArea(c)
			if area >= min_area:
				perimeter = cv.arcLength( c, True )
				points = cv.approxPolyDP( c, scale * perimeter, True )
				boxes_within.append(cv.boundingRect(points))
				area_within.append(area)
				cv.drawContours(self.im_contours, c, -1, (255, 255, 255), 2)					# <- DO RESEARCH

		return boxes_within, area_within

if __name__ == '__main__':
	import sys
	from os import path
	sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
	import cv_tools

	colorspace = Colorspace()
	sample_mode =  True

	if len(sys.argv) == 1:
		colorspace.createSliders()
	elif len(sys.argv) == 2:
		sample_mode =  False
		colorspace.loadSettings(sys.argv[1])
	else:
		raise Exception('Too many args')
		exit()

	cam = cv.VideoCapture(0)
	cam.set(cv.CAP_PROP_FRAME_WIDTH, 320)
	cam.set(cv.CAP_PROP_FRAME_HEIGHT, 240)

	while True:
		if sample_mode:
			colorspace.updateHSV()

		rec, frame = cam.read()
		if not rec:
			raise Exception('Cam is not recording')

		frame_blur = cv.GaussianBlur(frame, (9, 9), 150) 		# smoothes the noise
		frame_hsv = cv.cvtColor(frame_blur, cv.COLOR_BGR2HSV)	# convert BGR to HSV

		boxes, areas = colorspace.getMaskBoxesArea(frame, frame_hsv, 200, 0.1)	# get boxes and boxes area
		# boxes = colorspace.getMaskBoxes(frame, frame_hsv, 200, 0.1)	# get boxes
		offsets = cv_tools.getBoxesOffset(frame, boxes)			# get boxes offset from the center of the frame
		for i, offset in enumerate(offsets):
			print(i, offset)

		frame_out = cv_tools.drawBoxes(frame.copy(), boxes)
		frame_out = cv_tools.drawBoxesPos(frame_out, boxes)

		frame_grid = cv_tools.grid(frame, (2, 3),[
			frame_hsv, colorspace.im_contours, frame_out,
			colorspace.im_cut, colorspace.im_mask, colorspace.im_edges
		], 0.75)

		cv.imshow('grid', frame_grid)

		if cv.waitKey(1) & 0xFF == ord('q'):
			break

	cam.release()
	cv.destroyAllWindows()

	if sample_mode:
		colorspace.dumpSettings()
