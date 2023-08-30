import cv2
import mediapipe as mp
import csv


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

cap = cv2.VideoCapture(0)
hands = mphands.Hands()

# vector distence calculator
def vectorDistance(vector1, vector2):
    distance = 0
    for i in range(0, len(vector1)):
        distance += (vector1[i]-float(vector2[i+1]))**2
    return distance**(1/2)
    

while True:
    data, image = cap.read()
    
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    
    result = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mphands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
            
            #create hand vector
            vector = []
            for landmark in hand_landmarks.landmark:
                vector.append(landmark.x)
                vector.append(landmark.y)
                vector.append(landmark.z)
                
            distences = []
            file = open("LetterVectors.csv", "r") 
            reader = csv.reader(file) 
            for row in reader:
                distences.append([row[0], vectorDistance(vector, row)])
            file.close()
            
            #find smallest distences 
            def getDistence(item):
                return item[1]
            
            closest = sorted(distences, key=getDistence)
            charicter = closest[0][0]
            
            #find percentage of confidence for first, second and third closest
            first = closest[0]
            second = closest[1]
            third = closest[2]
            
            charicter = first[0] + " "
            #output charicter onto screen
            cv2.putText(image, charicter, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 3, cv2.LINE_AA)
            
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()