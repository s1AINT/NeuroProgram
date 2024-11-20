import time
from tkinter import Label

class FrameCounter:
    def __init__(self, master):
        self.label = Label(master, text="FPS: 0")
        self.frame_count = 0
        self.start_time = time.time()

    def increment(self):
        current_time = time.time()
        self.frame_count += 1
        elapsed_time = current_time - self.start_time

        if elapsed_time >= 1.0: 
            fps = self.frame_count / elapsed_time
            self.label.config(text=f"FPS: {int(fps)}")
            self.frame_count = 0
            self.start_time = current_time

    def reset(self):
        self.frame_count = 0
        self.start_time = time.time()
        self.label.config(text="FPS: 0")

    def grid(self, **kwargs):
        self.label.grid(**kwargs)
