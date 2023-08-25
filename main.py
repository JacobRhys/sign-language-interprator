import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

cap = cv2.VideoCapture(0)
hands = mphands.Hands()

#point distance calculator
def distance(point1, point2):
    return math.sqrt((point1.x-point2.x)**2+(point1.y-point2.y)**2+(point1.z-point2.z)**2)

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
            
            thumb_tip_position=hand_landmarks.landmark[mphands.HandLandmark.THUMB_TIP]
            index_finger_position=hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_nuckle=hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_PIP]
            index_finger_base=hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_MCP]
            middle_finger_position=hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_finger_nuckle=hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_PIP]
            middle_finger_base=hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_MCP]
            ring_finger_position=hand_landmarks.landmark[mphands.HandLandmark.RING_FINGER_TIP]
            ring_finger_nuckle=hand_landmarks.landmark[mphands.HandLandmark.RING_FINGER_PIP]
            ring_finger_base=hand_landmarks.landmark[mphands.HandLandmark.RING_FINGER_MCP]
            pinky_finger_position=hand_landmarks.landmark[mphands.HandLandmark.PINKY_TIP]
            pinky_finger_base=hand_landmarks.landmark[mphands.HandLandmark.PINKY_MCP]
            palm_top=hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_MCP]
            palm_bottom=hand_landmarks.landmark[mphands.HandLandmark.WRIST]
            palm_distance=distance(palm_top,palm_bottom)
            
            #clasifications of hand position            
            def isHorizontal():
                return ((palm_top.x-palm_bottom.x)**2>(palm_top.y-palm_bottom.y)**2)
            
            def isVertical():
                return not(isHorizontal())
            
            def isBehind(point1,point2):
                return (point1.z>point2.z)
            
            def isBetween(point1,point2,point3):
                return (point1.x<point2.x<point3.x or point3.x<point2.x<point1.x)
                
            def thumbPosition():
                if (distance(thumb_tip_position,palm_top)*1.5>palm_distance):
                    return "out"
                elif (distance(thumb_tip_position,middle_finger_position)*3.5<palm_distance or distance(thumb_tip_position,ring_finger_position)*3.5<palm_distance or distance(thumb_tip_position,ring_finger_base)*3.5<palm_distance):
                    return "in"
                else :
                    return "relaxed"
            
            def indexFingerUp():
                return (distance(index_finger_position,index_finger_base)*1.5>palm_distance)
            
            def middleFingerUp():
                return (distance(middle_finger_position,middle_finger_base)*1.5>palm_distance)
            
            def ringFingerUp():
                return (distance(ring_finger_position,ring_finger_base)*1.5>palm_distance)
            
            def pinkyFingerUp():
                return (distance(pinky_finger_position,pinky_finger_base)*1.5>palm_distance)
        
            
            #charicter recognition
            charicter = "?"
            
            def DecisionRoot():
                if indexFingerUp():
                    DecisionBranch_BCDGHKLOPQRUVWXZ()
                else:
                    DecisionBranch_AEFIJMNSTY()
                
            def DecisionBranch_BCDGHKLOPQRUVWXZ():
                global charicter
                charicter = "B"
                # add the left side of the decison tree here
                
            def DecisionBranch_AEFIJMNSTY():
                if thumbPosition=="in":
                    DecisionBranch_EMNST()
                else:
                    DecisionBranch_AFIJY()
            
            def DecisionBranch_EMNST():
                if isBehind(index_finger_position,thumb_tip_position):
                    DecisionBranch_EST()
                else:
                    DecisionBranch_MN()
            
            def DecisionBranch_EST():
                global charicter
                if isBetween(index_finger_nuckle,thumb_tip_position,middle_finger_nuckle):
                    charicter = "T"
                elif (distance(thumb_tip_position,pinky_finger_position < distance(thumb_tip_position,middle_finger_position))):
                    charicter = "E"
                else:
                    charicter = "S"
            
            def DecisionBranch_MN():
                global charicter
                if isBetween(ring_finger_nuckle,thumb_tip_position,middle_finger_nuckle):
                    charicter = "M"
                else:
                    charicter = "N"
            
            def DecisionBranch_AFIJY():
                if (pinkyFingerUp() and not ringFingerUp()):
                    DecisionBranch_IJY()
                else:
                    DecisionBranch_AF()
                    
            def DecisionBranch_IJY():
                global charicter
                if thumbPosition=="out":
                    charicter = "Y"
                elif (((pinky_finger_position.x-pinky_finger_base.x)**2)/2<(pinky_finger_position.y-pinky_finger_base.y)**2):
                    charicter = "J"
                else:
                    charicter = "I"
                    
            def DecisionBranch_AF():
                global charicter
                if middleFingerUp():
                    charicter = "F"
                else:
                    charicter = "A"
                    
            DecisionRoot()
            
            #output charicter onto screen
            cv2.putText(image, charicter, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 3, cv2.LINE_AA)
            cv2.putText(image, ("horisontal "+str(isHorizontal())), (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, ("thumb "+str(thumbPosition())), (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, ("index "+str(indexFingerUp())), (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, ("middle "+str(middleFingerUp())), (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, ("ring "+str(ringFingerUp())), (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, ("pinky "+str(pinkyFingerUp())), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
