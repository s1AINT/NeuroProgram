import onnxruntime as ort
import numpy as np

class EyeStateDetectionService:
    def __init__(self, model_path="models/open_closed_eye.onnx"):
        self.session = ort.InferenceSession(model_path)

    def detect_eye_state(self, eye_frame):
        if eye_frame is None or eye_frame.size == 0:
            print("Eye frame is empty or None.")
            return None

        input_tensor = self.preprocess(eye_frame)

        print(f"Input tensor shape: {input_tensor.shape}")
        print(f"Input tensor values range: min={input_tensor.min()}, max={input_tensor.max()}")

        output = self.session.run(None, {self.session.get_inputs()[0].name: input_tensor})

        print("Output probabilities:", output[0])

        predicted_state = "open" if np.argmax(output[0]) == 1 else "closed"
        print(f"Predicted eye state: {predicted_state}")
        
        return predicted_state

    def preprocess(self, eye_frame):
        input_tensor = eye_frame.astype(np.float32) / 255.0

        input_tensor = np.transpose(input_tensor, (2, 0, 1))  # [H, W, C] -> [C, H, W]

        input_tensor = np.expand_dims(input_tensor, axis=0)  # [C, H, W] -> [1, C, H, W]
        
        return input_tensor
