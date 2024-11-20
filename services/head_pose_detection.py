import onnxruntime as ort
import numpy as np
import cv2

class HeadPoseDetectionService:
    def __init__(self, model_path="models/fsanet_epoch_95.onnx"):
        self.session = ort.InferenceSession(model_path)
    
    def detect_head_pose(self, face_frame):
        input_tensor = self.preprocess(face_frame)
        output = self.session.run(None, {self.session.get_inputs()[0].name: input_tensor})

        #print(f"Model output: {output}")
        #print(f"Output shape: {np.array(output).shape}")

        if len(output) > 0 and output[0].shape == (1, 3):
            yaw, pitch, roll = output[0][0]
            #print(f"yaw: {yaw} pitch: {pitch} roll: {roll}")
            return {"yaw": yaw, "pitch": pitch, "roll": roll}
        else:
            #print(f"Unexpected output shape: {output[0].shape}")
            return None

    def preprocess(self, face_frame):
        resized_face = cv2.resize(face_frame, (64, 64))
        input_tensor = cv2.cvtColor(resized_face, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        input_tensor = np.transpose(input_tensor, (2, 0, 1)) 
        return np.expand_dims(input_tensor, axis=0) 
