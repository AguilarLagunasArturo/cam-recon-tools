import cv2 as cv
import numpy as np

def grid(base, dimentions, images, scale=0.5):
	# 1. SCALE IMAGE
	base = cv.resize(base, (0, 0), fx=scale, fy=scale)
	images = [cv.resize(image, (0, 0), fx=scale, fy=scale) for image in images]
	# 2. COMPLETE DIMENTIONS IF MISSING
	for i, image in enumerate(images):
		if len(image.shape) < 3:
			images[i] = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
	# 3. CREATE GRID
	missing = dimentions[0]*dimentions[1] - len(images)
	if missing < 0:
		raise Exception('Wrong grid dimentions')
	for i in range(missing):
		images.append(np.zeros(base.shape, dtype=np.uint8))
	grid = np.array(images);
	grid = grid.reshape( (dimentions[0], dimentions[1], base.shape[0], base.shape[1], base.shape[2]) )
	# 4. STACK IMAGES
	return np.vstack( [np.hstack(row[:]) for row in grid] )

def draw_boxes(edges, output, min_area=20, scale=0.2):
	contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)	# <- RESEARCH
	for c in contours:
		area = cv.contourArea(c)
		if area >= min_area:
			cv.drawContours(output, c, -1, (255, 255, 255), 2)						# <- RESEARCH
			perimeter = cv.arcLength(c, True)
			points = cv.approxPolyDP(c, scale * perimeter, True)
			x, y, w, h = cv.boundingRect(points)
			cv.rectangle(output, (x, y), (x + w, y + h), (130, 250, 255), 2)
	return output
