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

        # Шляхи до моделей YuNet
        model_paths = [
            "models/face_detection_yunet_2023mar.onnx",
            "models/face_detection_yunet_2023mar1.onnx",
            "models/face_detection_yunet_2023mar2.onnx",
            "models/face_detection_yunet_2023mar3.onnx"
        ]

        self.eye_state_detector = EyeStateDetectionService()
        self.head_pose_detector = HeadPoseDetectionService()
        self.attention_analysis_service = AttentionAnalysisService()

        self.detection_handler = DetectionHandler(
            face_detector_model_paths=model_paths,
            eye_state_detector=self.eye_state_detector,
            head_pose_detector=self.head_pose_detector,
            attention_analysis_service=self.attention_analysis_service,
            max_threads=2
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
        self.detection_handler.stop() 
        self.ui_handler.frame_counter.reset()
        self.running = False

    def update_frame(self):
        frame = self.video_handler.get_frame()
        if frame is not None:
            self.detection_handler.process_frame(frame, self.ui_handler)
            self.ui_handler.update_video_frame(frame)
        if self.running:
            self.root.after(10, self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
