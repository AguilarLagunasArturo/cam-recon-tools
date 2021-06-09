from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from time import sleep

'''
PiCamera settings: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/7
	[+] framerate
	[+] resolution
	[+] awb_mode
	[+] image_effect
	[+] exposure_mode
	[+] brightness	(0, 100)
	[+] contrast	(0, 100)
'''

class PiCam:
	def __init__(self, resolution=(320, 240), framerate=32, **kargs):
		self.camera = PiCamera()
		self.camera.framerate = framerate
		self.camera.resolution = resolution

		self.camera.brightness = 55
		self.camera.contrast = 10

		self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)

		for arg, value in kwargs.items():
			setattr(self.camera, arg, value)

		self.stream = self.camera.capture_continuous(
			self.rawCapture,
			format='bgr',
			use_video_port=True
		)

		self.current_frame = None
		self.stop = False

	def video_capture(self):
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

	def exposure_modes(self):
		for e in self.camera.EXPOSURE_MODES:
			print(e)

	def awb_modes(self):
		for e in self.camera.AWB_MODES:
			print(e)
