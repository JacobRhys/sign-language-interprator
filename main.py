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
            
            thumb_tip=hand_landmarks.landmark[mphands.HandLandmark.THUMB_TIP]
            index_finger_=hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_nuckle=hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_PIP]
            index_finger_base=hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_MCP]
            middle_finger_tip=hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_finger_nuckle=hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_PIP]
            middle_finger_base=hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_MCP]
            ring_finger_tip=hand_landmarks.landmark[mphands.HandLandmark.RING_FINGER_TIP]
            ring_finger_base=hand_landmarks.landmark[mphands.HandLandmark.RING_FINGER_MCP]
            pinky_finger_tip=hand_landmarks.landmark[mphands.HandLandmark.PINKY_TIP]
            pinky_finger_base=hand_landmarks.landmark[mphands.HandLandmark.PINKY_MCP]
            palm_top=hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_MCP]
            palm_bottom=hand_landmarks.landmark[mphands.HandLandmark.WRIST]
            palm_distance=distance(palm_top,palm_bottom)
            
            #clasifications of hand position            
            def isHorizontal():
                return (((palm_top.x-palm_bottom.x)*1.5)**2>(palm_top.y-palm_bottom.y)**2)
            
            def isVertical():
                return not(isHorizontal())
            
            def thumbPosition():
                if (distance(thumb_tip,palm_top)*1.5>palm_distance):
                    return "out"
                elif (distance(thumb_tip,middle_finger_tip)*3.5<palm_distance or distance(thumb_tip,ring_finger_tip)*3.5<palm_distance or distance(thumb_tip,ring_finger_base)*3.5<palm_distance):
                    return "in"
                else :
                    return "relaxed"
            
            def indexFingerUp():
                return (distance(index_finger_,index_finger_base)*1.8>palm_distance)
            
            def middleFingerUp():
                return (distance(middle_finger_tip,middle_finger_base)*1.8>palm_distance)
            
            def ringFingerUp():
                return (distance(ring_finger_tip,ring_finger_base)*1.8>palm_distance)
            
            def pinkyFingerUp():
                return (distance(pinky_finger_tip,pinky_finger_base)*1.8>palm_distance)
        
            
            #charicter recognition
            charicter = "?"
            
            if (isVertical() and (thumbPosition()=="relaxed") and (not indexFingerUp()) and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp())) : 
                charicter = "A"
            
            if (isVertical() and (thumbPosition()=="relaxed") and indexFingerUp() and middleFingerUp() and ringFingerUp() and pinkyFingerUp()):
                charicter = "B"
                
            if ((palm_top.y > index_finger_.y) and (palm_top.y > middle_finger_tip.y) and (palm_top.y > ring_finger_tip.y) and (palm_top.y > pinky_finger_tip.y) and 
               (palm_top.x > thumb_tip.x) and (palm_top.x > pinky_finger_tip.x)):
                charicter = "C"
            
            if (isVertical() and (thumbPosition()=="in") and indexFingerUp() and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp())) :
                charicter = "D"
                
            if (isVertical() and (thumbPosition()=="in") and (not indexFingerUp()) and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp())) :
                charicter = "E"
            
            if (isVertical() and middleFingerUp() and ringFingerUp() and pinkyFingerUp() and
                (distance(index_finger_,thumb_tip)*3<palm_distance)):
                charicter = "F"

            if (isHorizontal() and (thumbPosition()=="out") and indexFingerUp() and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp())):
                charicter = "G"
                
            if (isHorizontal() and (thumbPosition()=="out") and indexFingerUp() and middleFingerUp() and (not ringFingerUp()) and (not pinkyFingerUp())):
                charicter = "H"
            
            if (isVertical() and (thumbPosition()=="relaxed") and (not indexFingerUp()) and (not middleFingerUp()) and (not ringFingerUp()) and pinkyFingerUp()):
                if (((pinky_finger_tip.x-pinky_finger_base.x)*4)**2<(pinky_finger_tip.y-pinky_finger_base.y)**2):
                    charicter = "I"
                else:
                    charicter = "J"
                
            if (isVertical() and (thumbPosition()=="out") and indexFingerUp() and middleFingerUp() and (not ringFingerUp()) and (not pinkyFingerUp())):
                charicter = "K"
            
            if (isVertical() and (thumbPosition()=="out") and indexFingerUp() and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp())) :
                charicter = "L"
            
            if (isVertical() and (thumbPosition()=="in") and (not indexFingerUp()) and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp()) and
                (thumb_tip.z>ring_finger_tip.z)) :
                charicter = "M"
            
            if (isVertical() and (thumbPosition()=="in") and (not indexFingerUp()) and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp()) and
                (thumb_tip.z>ring_finger_tip.z) and (distance(index_finger_,middle_finger_tip)*1.2<distance(middle_finger_tip,ring_finger_tip))) :
                charicter = "N"
            
            if ((distance(index_finger_,thumb_tip)*3<palm_distance) and ((index_finger_base.z-pinky_finger_base.z)**2>(index_finger_base.x-pinky_finger_base.x)**2)):
                charicter = "O"
            
            if (isVertical() and indexFingerUp() and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp())
                and (index_finger_.y>index_finger_base.y)) :
                charicter = "p"
                
            if (isVertical() and indexFingerUp() and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp())
                and (index_finger_.y>index_finger_base.y)
                and (thumb_tip.y>index_finger_nuckle.y)) :
                charicter = "q"
            
            if (isVertical() and (thumbPosition()=="relaxed") and indexFingerUp() and middleFingerUp() and (not ringFingerUp()) and (not pinkyFingerUp())
                and index_finger_.x>middle_finger_tip.x) :
                charicter = "r"
            
            if (isVertical() and (thumbPosition()=="in") and (not indexFingerUp()) and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp())
                and (thumb_tip.y>index_finger_.y)) :
                charicter = "S"
            
            if (isVertical() and (not indexFingerUp()) and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp())
                and (middle_finger_nuckle.x>thumb_tip.x>index_finger_nuckle.x)) :
                charicter = "T"
                
            if (isVertical() and indexFingerUp() and middleFingerUp() and (not ringFingerUp()) and (not pinkyFingerUp())) :
                charicter = "U"
            
            if (isVertical() and (thumbPosition()=="relaxed") and indexFingerUp() and middleFingerUp() and (not ringFingerUp()) and (not pinkyFingerUp()) and (not index_finger_.x>middle_finger_tip.x)):
                charicter = "V"
            
            if (isVertical() and (thumbPosition()=="relaxed") and indexFingerUp() and middleFingerUp() and ringFingerUp() and (not pinkyFingerUp()) and (not index_finger_.x>middle_finger_tip.x)):
                charicter = "W"
                
            if (isVertical() and (thumbPosition()=="relaxed") and indexFingerUp() and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp())
                and (math.sqrt((index_finger_.y-index_finger_nuckle.y)**2)*1.5<distance(index_finger_,index_finger_nuckle))) :
                charicter = "X"

            if (isVertical and (thumbPosition()=="out") and (not indexFingerUp()) and (not middleFingerUp()) and (not ringFingerUp()) and pinkyFingerUp()):
                charicter = "Y"
            
            if (isVertical() and (thumbPosition()=="in") and indexFingerUp() and (not middleFingerUp()) and (not ringFingerUp()) and (not pinkyFingerUp())
                and ((index_finger_.x-index_finger_base.x)*4)**2>(index_finger_.y-index_finger_base.y)**2) :
                charicter = "Z"
            
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