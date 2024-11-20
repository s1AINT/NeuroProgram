import cv2
import numpy as np
import os
from datetime import datetime

SAVE_DIR = "cropped_images"
os.makedirs(SAVE_DIR, exist_ok=True)

def save_image(image, prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{prefix}_{timestamp}.png"
    filepath = os.path.join(SAVE_DIR, filename)
    cv2.imwrite(filepath, image)
    return filepath

def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height))

def crop_face_region(frame, bbox, ad=0.6):
    x, y, w, h = bbox
    cx, cy = x + w // 2, y + h // 2
    size = max(w, h)
    half_size = size // 2

    x_start = max(cx - half_size - int(ad * w), 0)
    y_start = max(cy - half_size - int(ad * h), 0)
    x_end = min(cx + half_size + int(ad * w), frame.shape[1])
    y_end = min(cy + half_size + int(ad * h), frame.shape[0])

    face_region = frame[y_start:y_end, x_start:x_end]
    if face_region.size > 0:
        face_region = resize_frame(face_region, 64, 64)
        save_image(face_region, "face")
    return face_region

def crop_eye_region(frame, eye_point, ad=0.3):
    eye_x, eye_y = eye_point
    half_size = 16

    x_start = max(eye_x - half_size - int(ad * half_size), 0) 
    y_start = max(eye_y - half_size - int(ad * half_size), 0)
    x_end = min(eye_x + half_size + int(ad * half_size), frame.shape[1])
    y_end = min(eye_y + half_size + int(ad * half_size), frame.shape[0])

    eye_region = frame[y_start:y_end, x_start:x_end]
    if eye_region.size > 0:
        eye_region = resize_frame(eye_region, 32, 32)
        save_image(eye_region, "eye")
    return eye_region
