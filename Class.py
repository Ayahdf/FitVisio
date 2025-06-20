import cv2
import mediapipe as mp
import numpy as np

def calculate_angle(a, b, c):
    a = np.array(a)  # Premier point
    b = np.array(b)  # Point central
    c = np.array(c)  # Troisième point
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle

def calculate_back_angle(shoulder, hip, knee):
    return calculate_angle(shoulder, hip, knee)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Choix de l'utilisateur
print("Choisissez une option :")
print("1. Utiliser la webcam")
print("2. Importer une vidéo depuis votre PC")
choice = input("Entrez 1 ou 2 : ")

if choice == "1":
    # Utiliser la webcam
    cap = cv2.VideoCapture(0)
elif choice == "2":
    # Importer une vidéo depuis le PC
    video_path = input("Entrez le chemin complet de la vidéo (par exemple : C:/Users/VotreNom/Videos/squat.mp4) : ")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la vidéo. Vérifiez le chemin du fichier.")
        exit()
else:
    print("Choix invalide. Veuillez relancer le programme.")
    exit()

squat_count = 0
squat_position = None
BACK_ANGLE_MIN = 90  # Angle minimum pour une inclinaison acceptable
BACK_ANGLE_MAX = 160  # Angle maximum pour une inclinaison acceptable

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Fin de la vidéo ou erreur de lecture.")
        break
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, 
               landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, 
                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, 
                 landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, 
                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        
        knee_angle = calculate_angle(hip, knee, ankle)
        back_angle = calculate_back_angle(shoulder, hip, knee)
        
        cv2.putText(image, f'Knee Angle: {int(knee_angle)}', (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, f'Back Angle: {int(back_angle)}', (50, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Vérifier si la position est correcte pour un squat
        if knee_angle < 90 and BACK_ANGLE_MIN <= back_angle <= BACK_ANGLE_MAX:
            if squat_position != "down":
                squat_position = "down"
                cv2.putText(image, "Squat correct!", (50, 150), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        elif knee_angle > 120 and squat_position == "down":
            squat_position = "up"
            squat_count += 1
        
        # Feedback sur la posture
        if knee_angle < 90 and back_angle < BACK_ANGLE_MIN:
            cv2.putText(image, "Redresse un peu ton dos!", (50, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        elif knee_angle < 90 and back_angle > BACK_ANGLE_MAX:
            cv2.putText(image, "Penche légèrement vers l'avant!", (50, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        elif knee_angle >= 90:
            cv2.putText(image, "Descends plus bas!", (50, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        # Afficher le nombre de squats
        cv2.putText(image, f'Squats: {squat_count}', (50, 250), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    cv2.imshow('Squat Counter', image)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()