import cv2
import datetime
from core.tracker import ExerciseTracker
from utils.video_input import VideoInput
from strategies.squat import SquatStrategy
from strategies.pushup import PushupStrategy

def main():
    print("=== IA Coach - Suivi d'Exercices ===")
    print("Initialisation...\n")
    
    # Initialiser le tracker
    tracker = ExerciseTracker()
    
    # Menu de sélection d'exercice
    print("Choisissez un exercice :")
    print("1. Squat")
    print("2. Push-up")
    exercise_choice = input("Entrez le numéro (1/2) : ")
    
    if exercise_choice == "1":
        tracker.set_strategy(SquatStrategy())
        print("\nMode Squat sélectionné")
    elif exercise_choice == "2":
        tracker.set_strategy(PushupStrategy())
        print("\nMode Push-up sélectionné")
    else:
        tracker.set_strategy(SquatStrategy())
        print("\nChoix invalide - Mode Squat par défaut")
    
    # Menu de sélection de source vidéo
    print("\nOptions de capture :")
    print("1. Utiliser la webcam")
    print("2. Charger une vidéo")
    source_choice = input("Entrez le numéro (1/2) : ")
    
    if source_choice == "1":
        cap = VideoInput.get_video_source(0)
        print("\nWebcam activée")
    else:
        video_path = input("\nEntrez le chemin complet de la vidéo : ")
        try:
            cap = VideoInput.get_video_source(video_path)
            print(f"\nVidéo chargée : {video_path}")
        except:
            print("\nErreur de chargement - Webcam par défaut")
            cap = VideoInput.get_video_source(0)
    
    # Instructions utilisateur
    print("\n=== Commandes ===")
    print("e : Démarrer/arrêter l'enregistrement")
    print("r : Réinitialiser les compteurs")
    print("q : Quitter l'application")
    print("=================\n")
    
    # Variables pour l'enregistrement
    recording_started = False
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("\nFin de la vidéo ou erreur de lecture")
                break
            
            # Traitement de la frame
            processed_frame = tracker.process_frame(frame)
            
            # Affichage
            cv2.imshow('IA Coach - ' + tracker.get_current_strategy().get_exercise_name(), processed_frame)
            
            # Gestion des touches
            key = cv2.waitKey(10) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('e'):
                if not recording_started:
                    output_file = f"{tracker.get_current_strategy().get_exercise_name()}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                    frame_size = VideoInput.get_frame_size(cap)
                    tracker.start_recording(output_file, frame_size)
                    recording_started = True
                    print(f"\nEnregistrement démarré : {output_file}")
                else:
                    tracker.stop_recording()
                    recording_started = False
                    print("\nEnregistrement terminé")
            elif key == ord('r'):
                tracker.get_current_strategy().reset_counts()
                print("\nCompteurs réinitialisés")
                
    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"\nErreur : {str(e)}")
    finally:
        # Nettoyage
        cap.release()
        if recording_started:
            tracker.stop_recording()
        cv2.destroyAllWindows()
        
        # Affichage des résultats finaux
        counts = tracker.get_current_strategy().get_counts()
        print("\n=== Résultats ===")
        print(f"Exercice : {tracker.get_current_strategy().get_exercise_name()}")
        print(f"Répétitions totales : {counts['total']}")
        print(f"Forme correcte : {counts['correct']}")
        print(f"Forme incorrecte : {counts['incorrect']}")
        if counts['total'] > 0:
            print(f"Taux de réussite : {(counts['correct']/counts['total'])*100:.1f}%")
        print("=================")

if __name__ == "__main__":
    main()