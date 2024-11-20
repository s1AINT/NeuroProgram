import cv2

def get_available_cameras():
    index = 0
    available_cameras = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            available_cameras.append(index)
        cap.release()
        index += 1
    return available_cameras

def open_camera(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise ValueError(f"Не вдалося відкрити камеру з індексом {camera_index}")
    return cap

def release_camera(cap):
    cap.release()
    cv2.destroyAllWindows()
