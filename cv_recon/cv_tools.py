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

def drawOffset(im, boxes):
	cv.line(
		im,
		(0, int(im.shape[0]/2)),
		(im.shape[1], int(im.shape[0]/2)),
		(0, 255, 0), 2)
	cv.line(
		im,
		(int(im.shape[1]/2), 0),
		(int(im.shape[1]/2), im.shape[0] ),
		(0, 255, 0), 2)

	for box in boxes:
		x, y, w, h = box
		xc, yc = (x + int(w/2), y + int(h/2))
		cv.circle( im, (xc, yc) , 1, (130, 250, 255), 2 )
		cv.rectangle( im, (x, y), (x + w, y + h), (255, 250, 255), 2 )
		cv.line( im, (xc, yc), (xc + int( im.shape[1]/2 - xc ), yc), (130, 250, 255), 1 )
		cv.line( im, (xc, yc), (xc, yc + int( im.shape[0]/2 - yc )), (130, 250, 255), 1 )

	return im
