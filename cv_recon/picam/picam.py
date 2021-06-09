from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from time import sleep

class PiCam:
	def __init__(self, resolution=(320, 240), framerate=32, **kargs):
		self.camera = PiCamera()
		self.camera.framerate = framerate
		self.camera.resolution = resolution

		self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)

		for arg, value in kargs.items():
			setattr(self.camera, arg, value)

		self.stream = self.camera.capture_continuous(
			self.rawCapture,
			format='bgr',
			use_video_port=True
		)

		self.current_frame = None
		self.stop = False

	def videoCapture(self):
		cam_thread = Thread(target=self.__update, args=(), daemon=True)
		cam_thread.start()

	def __update(self):
		for frame in self.stream:
			self.current_frame = frame.array
			self.rawCapture.truncate(0)
			if self.stop:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				break

	def release(self):
		self.stop = True

	def effects(self):
		for e in self.camera.IMAGE_EFFECTS:
			print(e)

	def exposureModes(self):
		for e in self.camera.EXPOSURE_MODES:
			print(e)

	def awbModes(self):
		for e in self.camera.AWB_MODES:
			print(e)
