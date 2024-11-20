import cv2

class VideoHandler:
    def __init__(self):
        self.camera = None
        self.running = False

    def start_camera(self, index):
        if self.camera:
            self.camera.release()
        self.camera = cv2.VideoCapture(index)
        if not self.camera.isOpened():
            raise RuntimeError("Could not open selected camera.")
        self.running = True

    def stop_camera(self):
        self.running = False
        if self.camera:
            self.camera.release()

    def get_frame(self):
        if self.running and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                return cv2.resize(frame, (640, 480))
        return None
