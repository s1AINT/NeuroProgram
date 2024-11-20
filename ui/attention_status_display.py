import tkinter as tk
from tkinter import Label, Frame

class AttentionStatusDisplay:
    def __init__(self, master):
        self.frame = Frame(master)
        
        self.attention_status_label = Label(self.frame, text="Attention Level: N/A")
        self.attention_status_label.grid(row=0, column=0, sticky="w")

        self.blocks_status_labels = []

    def update_attention_status(self, status):
        self.attention_status_label.config(text=f"Attention Level: {status}")

    def update_blocks_status(self, block):
        if len(self.blocks_status_labels) >= 5:
            old_label = self.blocks_status_labels.pop(0)
            old_label.destroy()

        block_status_label = Label(self.frame, text=f"Block Status: {block.status}", font=("Arial", 10, "bold"))
        block_status_label.grid(sticky="w")  

        self.blocks_status_labels.append(block_status_label)

        for sub_block in block.sub_blocks:
            sub_block_label = Label(self.frame, text=f"  SubBlock Status: {sub_block.status}", font=("Arial", 8))
            sub_block_label.grid(sticky="w", padx=10)
            self.blocks_status_labels.append(sub_block_label)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
