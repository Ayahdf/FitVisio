import cv2
from core.tracker import ExerciseTracker
from utils.video_input import VideoInput
from strategies.squat import SquatStrategy

def main():
    # Set up video source
    cap = VideoInput.get_video_source()
    
    # Create and set up exercise tracker with SquatStrategy
    tracker = ExerciseTracker()
    tracker.set_strategy(SquatStrategy())
    
    # Main loop
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Fin de la vidéo ou erreur de lecture.")
            break
        
        processed_frame = tracker.process_frame(frame)
        
        cv2.imshow(f'{tracker.strategy.get_exercise_name()} Counter', processed_frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()