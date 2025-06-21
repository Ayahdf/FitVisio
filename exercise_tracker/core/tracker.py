import cv2
import mediapipe as mp

class ExerciseTracker:
    def __init__(self, strategy=None):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.strategy = strategy
        self.is_recording = False
        self.video_writer = None

    def set_strategy(self, strategy):
        self.strategy = strategy

    def start_recording(self, output_path, frame_size, fps=30):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
        self.is_recording = True

    def stop_recording(self):
        if self.is_recording:
            self.video_writer.release()
            self.is_recording = False

    def process_frame(self, frame):
        try:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                if self.strategy:
                    image = self.strategy.process_landmarks(results.pose_landmarks.landmark, self.mp_pose, image)
                self.mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

            if self.is_recording and self.video_writer is not None:
                self.video_writer.write(image)
                cv2.putText(image, "REC", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            return image
        except Exception as e:
            print(f"Error processing frame: {e}")
            return frame

    def get_current_strategy(self):
        return self.strategy