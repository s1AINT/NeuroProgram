from queue import Queue, Empty
from threading import Thread, Lock
from utils.frame_utils import crop_face_region, crop_eye_region
from services.face_detection import FaceDetectionService
import time

class MultiThreadedFrameProcessor:
    def __init__(self, model_paths, eye_state_detector, head_pose_detector, max_threads=4):
        self.frame_queue = Queue(maxsize=max_threads)
        self.result_queue = Queue()
        self.threads = []
        self.max_threads = max_threads
        self.detectors = [FaceDetectionService(model_path) for model_path in model_paths]
        self.eye_state_detector = eye_state_detector
        self.head_pose_detector = head_pose_detector
        self.lock = Lock()

    def start_threads(self):
        for i in range(self.max_threads):
            thread = Thread(target=self.process_frame_worker, args=(self.detectors[i],))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def stop_threads(self):
        for _ in range(self.max_threads):
            self.frame_queue.put(None)
        for thread in self.threads:
            thread.join()

    def add_frame(self, frame_id, frame):
        if not self.frame_queue.full():
            self.frame_queue.put((frame_id, frame))
        else:
            with self.lock:
                print(f"Frame {frame_id} dropped due to full queue.")

    def get_results(self):
        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get())
        return results

    def process_frame_worker(self, detector):
        while True:
            task = self.frame_queue.get()
            if task is None:
                break

            frame_id, frame = task
            try:
                faces = detector.detect_faces(frame)
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
                self.result_queue.put((frame_id, results))
            except Exception as e:
                print(f"Error processing frame {frame_id}: {e}")
            finally:
                self.frame_queue.task_done()