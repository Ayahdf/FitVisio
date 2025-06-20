import cv2
from strategies.base import ExerciseStrategy
from utils.angle_calculator import calculate_angle

class SquatStrategy(ExerciseStrategy):
    def __init__(self):
        super().__init__()
        self.BACK_ANGLE_MIN = 90  # Minimum angle for acceptable back inclination
        self.BACK_ANGLE_MAX = 160  # Maximum angle for acceptable back inclination
    
    def get_exercise_name(self):
        return "Squat"
    
    def process_landmarks(self, landmarks, mp_pose, image):
        hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, 
               landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, 
                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, 
                 landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, 
                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        
        knee_angle = calculate_angle(hip, knee, ankle)
        back_angle = calculate_angle(shoulder, hip, knee)
        
        cv2.putText(image, f'Knee Angle: {int(knee_angle)}', (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, f'Back Angle: {int(back_angle)}', (50, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Check if position is correct for a squat
        if knee_angle < 90 and self.BACK_ANGLE_MIN <= back_angle <= self.BACK_ANGLE_MAX:
            if self.position != "down":
                self.position = "down"
                cv2.putText(image, "Squat correct!", (50, 150), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        elif knee_angle > 120 and self.position == "down":
            self.position = "up"
            self.rep_count += 1
        
        # Feedback on posture
        if knee_angle < 90 and back_angle < self.BACK_ANGLE_MIN:
            cv2.putText(image, "Redresse un peu ton dos!", (50, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        elif knee_angle < 90 and back_angle > self.BACK_ANGLE_MAX:
            cv2.putText(image, "Penche légèrement vers l'avant!", (50, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        elif knee_angle >= 90:
            cv2.putText(image, "Descends plus bas!", (50, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        return image