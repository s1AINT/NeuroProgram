import cv2
from tkinter import ttk

class CameraSelector:
    def __init__(self, master):
        self.combo = ttk.Combobox(master)
        self.combo['values'] = self.get_available_cameras()
        self.combo.current(0)
    
    def get_available_cameras(self):
        available_cameras = []
        for index in range(10):
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                available_cameras.append(f"Camera {index}")
                cap.release()
        return available_cameras
    
    def get_selected_camera_index(self):
        return int(self.combo.get().split()[1])
    
    def grid(self, **kwargs):
        self.combo.grid(**kwargs)
