import cv2
import numpy as np
from utils.frame_utils import crop_face_region, crop_eye_region

class FrameProcessingService:
    def __init__(self, face_detector, eye_state_detector, head_pose_detector):
        self.face_detector = face_detector
        self.eye_state_detector = eye_state_detector
        self.head_pose_detector = head_pose_detector

    def process_frame(self, frame):
        faces = self.face_detector.detect_faces(frame)
        results = []

        for face in faces:
            x, y, w, h = face["face_box"]

            face_region = crop_face_region(frame, (x, y, w, h))

            head_pose = self.head_pose_detector.detect_head_pose(face_region)

            left_eye_region = crop_eye_region(frame, face["landmarks"][0])
            right_eye_region = crop_eye_region(frame, face["landmarks"][1])

            left_eye_state = self.eye_state_detector.detect_eye_state(left_eye_region)
            right_eye_state = self.eye_state_detector.detect_eye_state(right_eye_region)

            results.append({
                "face_box": (x, y, w, h),
                "landmarks": face["landmarks"],
                "head_pose": head_pose,
                "left_eye": {
                    "state": left_eye_state,
                    "region": left_eye_region
                },
                "right_eye": {
                    "state": right_eye_state,
                    "region": right_eye_region
                }
            })

        return results
