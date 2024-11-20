import tkinter as tk
from PIL import Image, ImageTk
import cv2
from ui.camera_selector import CameraSelector
from ui.control_buttons import ControlButtons
from ui.frame_counter import FrameCounter
from ui.attention_status_display import AttentionStatusDisplay

class UIHandler:
    def __init__(self, root, start_callback, stop_callback):
        self.root = root
        self.root.title("Attention Detection")
        self.root.geometry("800x600")
        self.configure_layout()

        self.camera_selector = CameraSelector(root)
        self.camera_selector.grid(row=0, column=0, sticky="nw")

        self.buttons = ControlButtons(root, start_callback, stop_callback)
        self.buttons.grid(row=0, column=0, sticky="ne")

        self.frame_counter = FrameCounter(root)
        self.frame_counter.grid(row=0, column=1, sticky="nw")

        self.attention_status_display = AttentionStatusDisplay(root)
        self.attention_status_display.grid(row=0, column=1, sticky="ne")

        self.video_label = tk.Label(root)
        self.video_label.grid(row=1, column=0, sticky="nsew")

        self.attention_status_display = AttentionStatusDisplay(root)
        self.attention_status_display.grid(row=1, column=1, sticky="nsew")

    def configure_layout(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=4)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)

    def update_video_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(frame_image)
        self.video_label.config(image=frame_tk)
        self.video_label.image = frame_tk
