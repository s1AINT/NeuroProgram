import time

import cv2
from patterns.block_structure import FrameStatus, SubBlock, Block
from services.multi_threaded_frame_processor import MultiThreadedFrameProcessor

class DetectionHandler:
    def __init__(self, face_detector_model_paths, eye_state_detector, head_pose_detector, attention_analysis_service, max_threads=4):
        self.processor = MultiThreadedFrameProcessor(
            model_paths=face_detector_model_paths,
            eye_state_detector=eye_state_detector,
            head_pose_detector=head_pose_detector,
            max_threads=max_threads
        )
        self.attention_analysis_service = attention_analysis_service
        self.frame_statuses = []
        self.sub_blocks = []
        self.sub_block_start_time = time.time()
        self.sub_block_duration = 1
        self.frame_id = 0
        self.processor.start_threads()

    def process_frame(self, frame, ui_handler):
        self.processor.add_frame(self.frame_id, frame)
        self.frame_id += 1

        results = self.processor.get_results()
        ui_handler.frame_counter.increment()

        for frame_id, result_list in results:
            for result in result_list:
                self.draw_detections(frame, result)
                frame_status = self.determine_frame_status(result)
                self.frame_statuses.append(frame_status)

        self.aggregate_sub_blocks(ui_handler)

    def draw_detections(self, frame, result):
        x, y, w, h = result["face_box"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        landmarks = result["landmarks"]
        colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 0, 255), (0, 255, 255)]
        for idx, point in enumerate(landmarks):
            cv2.circle(frame, tuple(point), 2, colors[idx], 2)

    def determine_frame_status(self, detection):
        head_pose = detection["head_pose"]
        left_eye = detection["left_eye"]["state"]
        right_eye = detection["right_eye"]["state"]

        if head_pose:
            pitch = head_pose["pitch"]
            if pitch < -25:
                return FrameStatus.HEAD_TURNED_LEFT
            elif pitch > 25:
                return FrameStatus.HEAD_TURNED_RIGHT
            else:
                return FrameStatus.HEAD_STRAIGHT

        if left_eye == "closed" and right_eye == "closed":
            return FrameStatus.CLOSED_EYES
        elif left_eye == "open" or right_eye == "open":
            return FrameStatus.OPEN_EYES

        return FrameStatus.FACE_NOT_DETECTED

    def aggregate_sub_blocks(self, ui_handler):
        current_time = time.time()

        if len(self.frame_statuses) >= 30 or (current_time - self.sub_block_start_time >= self.sub_block_duration):
            sub_block = SubBlock(self.frame_statuses)
            self.sub_blocks.append(sub_block)
            self.frame_statuses = []
            self.sub_block_start_time = current_time

            if len(self.sub_blocks) >= 5:
                block = Block(self.sub_blocks)
                block_status = block.status

                ui_handler.attention_status_display.update_attention_status(block_status)
                ui_handler.attention_status_display.update_blocks_status(block)

                self.sub_blocks = []

    def stop(self):
        self.processor.stop_threads()