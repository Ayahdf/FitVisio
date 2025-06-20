from abc import ABC, abstractmethod

class ExerciseStrategy(ABC):
    def __init__(self):
        self.rep_count = 0
        self.position = None
    
    @abstractmethod
    def process_landmarks(self, landmarks, mp_pose, image):
        pass
    
    @abstractmethod
    def get_exercise_name(self):
        pass
    
    def get_rep_count(self):
        return self.rep_count