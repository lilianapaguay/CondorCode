from typing import Iterator, Union

import cv2


class WebcamStream:
	def __init__(self, source: Union[int, str] = 0):
		self.source = source
		self.capture = cv2.VideoCapture(source)
		if not self.capture.isOpened():
			raise RuntimeError(f"Unable to open webcam source: {source}")

	def frames(self) -> Iterator:
		while True:
			ok, frame = self.capture.read()
			if not ok:
				break
			yield frame

	def close(self) -> None:
		if self.capture is not None:
			self.capture.release()
