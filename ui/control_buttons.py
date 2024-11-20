from tkinter import Button

class ControlButtons:
    def __init__(self, master, start_callback, stop_callback):
        self.start_button = Button(master, text="Start", command=start_callback)
        self.stop_button = Button(master, text="Stop", command=stop_callback)
    
    def grid(self, **kwargs):
        self.start_button.grid(row=0, column=0, sticky="w", padx=5)
        self.stop_button.grid(row=0, column=1, sticky="e", padx=5)
