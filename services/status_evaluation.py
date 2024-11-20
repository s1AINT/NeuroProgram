class StatusEvaluationService:
    def evaluate_frame_status(self, eye_state, head_pose, face_detected):
        if not face_detected:
            return "FaceNotDetected"

        if eye_state == "closed":
            return "ClosedEyes"

        yaw, _, _ = head_pose
        if yaw < -15:
            return "HeadTurnedLeft"
        elif yaw > 15:
            return "HeadTurnedRight"

        return "OpenEyes"