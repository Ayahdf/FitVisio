import cv2

class VideoInput:
    @staticmethod
    def get_video_source():
        print("Choisissez une option :")
        print("1. Utiliser la webcam")
        print("2. Importer une vidéo depuis votre PC")
        choice = input("Entrez 1 ou 2 : ")
        
        if choice == "1":
            # Use webcam
            return cv2.VideoCapture(0)
        elif choice == "2":
            # Import video from PC
            video_path = input("Entrez le chemin complet de la vidéo (par exemple : C:/Users/VotreNom/Videos/exercise.mp4) : ")
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print("Erreur : Impossible d'ouvrir la vidéo. Vérifiez le chemin du fichier.")
                exit()
            return cap
        else:
            print("Choix invalide. Veuillez relancer le programme.")
            exit()
            