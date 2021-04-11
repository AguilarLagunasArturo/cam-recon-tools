from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from time import sleep

class PiCamStream:
	def __init__(self, resolution=(320, 240), fps=32, **kargs):
		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.camera.brightness = 55
		self.camera.contrast = 10

		self.fps = fps
		self.rawCapture = PiRGBArray(self.camera, size=resolution)

		self.stream = self.camera.capture_continuous(
			self.rawCapture,
			format='bgr',
			use_video_port=True
		)

		self.current_frame = None
		self.stop = False

	def start(self):
		cam_thread = Thread(target=self.update, args=())
		cam_thread.daemon = True
		cam_thread.start()

	def update(self):
		for frame in self.stream:
			self.current_frame = frame.array
			self.rawCapture.truncate(0)
			if self.stop:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				break

	def close(self):
		self.stop = True

