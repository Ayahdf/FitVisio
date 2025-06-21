import cv2
from strategies.base import ExerciseStrategy
from utils.angle_calculator import calculate_angle

class PushupStrategy(ExerciseStrategy):
    def __init__(self):
        super().__init__()
        self.ELBOW_ANGLE_MIN = 70
        self.ELBOW_ANGLE_MAX = 100
        self.BODY_ANGLE_MIN = 160
        self.current_form = "unknown"
        self.elbow_angle = 0
        self.body_angle = 0

    def get_exercise_name(self):
        return "Push-up"

    def check_correct_form(self):
        return self.current_form

    def process_landmarks(self, landmarks, mp_pose, image):
        try:
            # Get keypoints (use left side by default)
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            # Calculate angles
            self.elbow_angle = calculate_angle(shoulder, elbow, wrist)
            self.body_angle = calculate_angle(hip, shoulder, elbow)

            # Check push-up position
            if self.elbow_angle < self.ELBOW_ANGLE_MAX:
                if (self.ELBOW_ANGLE_MIN <= self.elbow_angle <= self.ELBOW_ANGLE_MAX and 
                    self.body_angle > self.BODY_ANGLE_MIN):
                    self.current_form = "correct"
                    form_color = (0, 255, 0)  # Green
                    feedback = "Bonne forme!"
                else:
                    self.current_form = "incorrect"
                    form_color = (0, 0, 255)  # Red
                    feedback = "Corrigez votre posture"

                if self.position != "down":
                    self.position = "down"
                    if self.current_form == "correct":
                        self.correct_count += 1
                    else:
                        self.incorrect_count += 1
            
            elif self.elbow_angle > 160 and self.position == "down":
                self.position = "up"
                self.rep_count += 1

            # Display info
            cv2.putText(image, f"Push-ups: {self.rep_count}", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            cv2.putText(image, f"Correct: {self.correct_count}", (20, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(image, f"Incorrect: {self.incorrect_count}", (20, 120), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.putText(image, f"Coudes: {int(self.elbow_angle)}°", (20, 160), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(image, f"Corps: {int(self.body_angle)}°", (20, 200), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(image, feedback, (20, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, form_color, 2)

            return image
        except Exception as e:
            print(f"Error in push-up processing: {e}")
            return image