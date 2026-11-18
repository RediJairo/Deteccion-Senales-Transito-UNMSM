import cv2


class CameraController:

    def __init__(self):
        self.cap = None

    def iniciar(self):
        self.cap = cv2.VideoCapture(0)
        return self.cap.isOpened()

    def leer(self):
        if self.cap is None:
            return False, None
        return self.cap.read()

    def detener(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None