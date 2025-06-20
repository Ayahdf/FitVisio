import cv2
import mediapipe as mp

class ExerciseTracker:
    def __init__(self, strategy=None):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        self.strategy = strategy
        
    def set_strategy(self, strategy):
        self.strategy = strategy
        
    def process_frame(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # Process with current strategy
            if self.strategy:
                image = self.strategy.process_landmarks(landmarks, self.mp_pose, image)
                
                # Display rep count
                cv2.putText(image, f'{self.strategy.get_exercise_name()}: {self.strategy.get_rep_count()}', 
                            (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
            
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            
        return image