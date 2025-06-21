from abc import ABC, abstractmethod

class ExerciseStrategy(ABC):
    def __init__(self):
        self.rep_count = 0
        self.position = "up"
        self.correct_count = 0
        self.incorrect_count = 0

    @abstractmethod
    def get_exercise_name(self):
        pass

    @abstractmethod
    def process_landmarks(self, landmarks, mp_pose, image):
        pass

    def check_correct_form(self):
        return "unknown"

    def get_counts(self):
        return {
            'correct': self.correct_count,
            'incorrect': self.incorrect_count,
            'total': self.rep_count
        }

    def reset_counts(self):
        self.rep_count = 0
        self.correct_count = 0
        self.incorrect_count = 0