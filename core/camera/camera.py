import cv2


class Camera:

    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = None

    def open(self):
        self.cap = cv2.VideoCapture(self.camera_id)
        return self.cap.isOpened()

    def read(self):
        if self.cap is None:
            return False, None

        return self.cap.read()

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None