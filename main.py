import tkinter as tk
from handlers.video_handler import VideoHandler
from handlers.detection_handler import DetectionHandler
from ui.ui_handler import UIHandler
from services.face_detection import FaceDetectionService
from services.eye_state_detection import EyeStateDetectionService
from services.head_pose_detection import HeadPoseDetectionService
from services.attention_analysis import AttentionAnalysisService

class App:
    def __init__(self, root):
        self.root = root
        
        self.face_detector = FaceDetectionService()
        self.eye_state_detector = EyeStateDetectionService()
        self.head_pose_detector = HeadPoseDetectionService()
        self.attention_analysis_service = AttentionAnalysisService()
        
        self.detection_handler = DetectionHandler(
            face_detector=self.face_detector,
            eye_state_detector=self.eye_state_detector,
            head_pose_detector=self.head_pose_detector,
            attention_analysis_service=self.attention_analysis_service
        )
        
        self.video_handler = VideoHandler()
        self.ui_handler = UIHandler(root, self.start, self.stop)

        self.running = False

    def start(self):
        try:
            selected_index = self.ui_handler.camera_selector.get_selected_camera_index()
            self.video_handler.start_camera(selected_index)
            self.running = True
            self.update_frame()
        except RuntimeError as e:
            print(e)

    def stop(self):
        self.video_handler.stop_camera()
        self.ui_handler.frame_counter.reset()
        self.running = False

    def update_frame(self):
        frame = self.video_handler.get_frame()
        if frame is not None:
            results = self.detection_handler.process_frame(frame, self.ui_handler)
            self.ui_handler.update_video_frame(frame)
        if self.running:
            self.root.after(10, self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
