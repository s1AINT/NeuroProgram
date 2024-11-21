import tkinter as tk
from PIL import Image, ImageTk
import cv2
from ui.attention_status_display import AttentionStatusDisplay
from ui.camera_selector import CameraSelector
from ui.control_buttons import ControlButtons
from ui.frame_counter import FrameCounter


class UIHandler:
    def __init__(self, root, start_callback, stop_callback):
        self.root = root
        self.root.title("Attention Detection")
        self.root.geometry("1200x700")
        self.configure_layout()

        self.camera_selector = CameraSelector(root)
        self.camera_selector.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        self.buttons = ControlButtons(root, start_callback, stop_callback)
        self.buttons.grid(row=0, column=1, sticky="ne", padx=5, pady=5)

        self.frame_counter = FrameCounter(root)
        self.frame_counter.grid(row=0, column=0, sticky="se", padx=5, pady=5)

        self.attention_status_display = AttentionStatusDisplay(root)
        self.attention_status_display.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        self.video_label = tk.Label(root, text="Original Video", bg="black", fg="white")
        self.video_label.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    def configure_layout(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=4)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_columnconfigure(2, weight=1)

    def update_video_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(frame_image)
        self.video_label.config(image=frame_tk)
        self.video_label.image = frame_tk
