import cv2 as cv
import numpy as np

class Features:
	def __init__(self, im_source=None, features=500):
		if im_source is None:
			raise Exception('Must input a grayscale image')
		self.corners = np.float32([
			[0, 0], [0, im_source.shape[0]],
			[im_source.shape[1], im_source.shape[0]], [im_source.shape[1], 0]
		]).reshape(-1, 1, 2)
		self.bf = cv.BFMatcher()
		self.features = features
		self.orb = cv.ORB_create(nfeatures=features)
		self.kp1, self.des1 = self.orb.detectAndCompute(im_source, None)
		self.im_source_kp = cv.drawKeypoints(im_source.copy(), self.kp1, None)
		self.im_source = im_source

		self.kp2, self.des2 = (None, None)
		self.im_target_kp = None
		self.im_target = None


	def loadTarget(self, im):
		self.im_target = im.copy()

	def getMatches(self, distance):
		self.kp2, self.des2 = self.orb.detectAndCompute(self.im_target, None)
		self.im_target_kp = cv.drawKeypoints(self.im_target.copy(), self.kp2, None)

		if len(self.kp2) <= 1:
			raise Exception('Not enough keypoints in target')

		matches = self.bf.knnMatch(self.des1, self.des2, k=2) # RESEARCH

		good = []
		for m, n in matches:
			if m.distance < distance *  n.distance:
				good.append( m )
		return good

	def matchPoints(self, matches):
		return cv.drawMatchesKnn(
			self.im_source, self.kp1,
			self.im_target, self.kp2,
			[matches], None, flags=2)

	def drawPoly(self, im_out, matches, min_matches):
		if len(matches) >= min_matches:
			src_points = np.float32(
				[self.kp1[m.queryIdx].pt for m in matches]
			).reshape(-1, 1, 2)
			dst_points = np.float32(
				[self.kp2[m.trainIdx].pt for m in matches]
			).reshape(-1, 1, 2)

			matrix, mask = cv.findHomography(src_points, dst_points, cv.RANSAC, 5) # RESEARCH

			if matrix is None:
				raise Exception('Cannot find homography in matches')

			des = cv.perspectiveTransform(self.corners, matrix)
			return cv.polylines(im_out, [np.int32(des)], True, (0, 255, 0), 3)

if __name__ == '__main__':
	import sys
	from os import path
	sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
	import cv_tools

	if len(sys.argv) == 2:
		im_source = cv.imread(sys.argv[1], 0)
		#im_source = cv.resize(im_source, (0, 0), fx=0.5, fy=0.5)
	elif len(sys.argv) == 1:
		raise Exception('Must input a path to an image')
		exit()
	else:
		raise Exception('Too many args')
		exit()

	my_feature = Features(im_source, 1000)

	cam = cv.VideoCapture(0)
	while True:
		if cv.waitKey(1) & 0xFF == ord('q'):
			break

		rec, frame = cam.read()
		im_target = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		frame_matches = None

		my_feature.loadTarget(frame)

		try:
			matches = my_feature.getMatches(0.75)
			frame_matches = my_feature.matchPoints(matches)
			my_feature.drawPoly(frame, matches, 20)
		except Exception as e:
			cv.imshow('image poly', frame)
			print(e)
			continue

		if frame_matches is not None:
			cv.imshow('image matches', frame_matches)
		cv.imshow('image poly', frame)

	cam.release()
	cv.destroyAllWindows()
