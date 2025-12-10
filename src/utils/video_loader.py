import cv2

class VideoLoader:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError(f'Cannot open video source {source}')

    def read_frame(self):
        return self.cap.read()

    def release(self):
        self.cap.release()
