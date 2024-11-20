import cv2 as cv
import numpy as np
from yunet import YuNet

class FaceDetectionService:
    def __init__(self, model_path="models/face_detection_yunet_2023mar.onnx"):
        self.model = YuNet(
            modelPath=model_path,
            inputSize=[320, 320],
            confThreshold=0.9,
            nmsThreshold=0.3,
            topK=5000,
            backendId=cv.dnn.DNN_BACKEND_OPENCV,
            targetId=cv.dnn.DNN_TARGET_CPU
        )
    
    def detect_faces(self, frame):
        h, w, _ = frame.shape
        self.model.setInputSize([w, h])
        results = self.model.infer(frame)
        return self.postprocess(results)

    def postprocess(self, results):
        detections = []
        for det in results:
            conf = det[-1]
            if conf > 0.1:
                x, y, width, height = det[:4].astype(int)
                landmarks = det[4:14].astype(int).reshape((5, 2))
                detections.append({
                    "face_box": (x, y, width, height),
                    "landmarks": landmarks
                })
        return detections
