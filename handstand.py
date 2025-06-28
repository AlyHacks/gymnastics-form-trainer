import cv2 as cv
import numpy as np
import mediapipe as mp
import math

cap = cv.VideoCapture(1)

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose()


while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)


    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
        l_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        r_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]#the results is object returning detected landmakrs, 
    # the pose_landmarks is referring to the 33 landmarks on the body
    # the .landmark is the access a specific landmark, usually we say .landmark[27], or a number
    #but in this case, we're referring to it as mp_pose.PoseLandmark.LEFT_HIP etc.
        l_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        r_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    
        l_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        r_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
        l_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
        r_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]

        h = frame.shape[0]
        w = frame.shape[1]

        lhip_coord = (int(l_hip.x*w), int(l_hip.y*h))
        rhip_coord = (int(r_hip.x*w), int(r_hip.y*h))
        lshoulder_coord = (int(l_shoulder.x*w), int(l_shoulder.y*h))
        rshoulder_coord = (int(r_shoulder.x*w), int(r_shoulder.y*h))
        lknee_coord = (int(l_knee.x*w), int(l_knee.y*h))
        rknee_coord = (int(r_knee.x*w), int(r_knee.y*h))
        lankle_coord = (int(l_ankle.x*w), int(l_ankle.y*h))
        rankle_coord = (int(r_ankle.x*w), int(r_ankle.y*h))

    #vector time

        lvec_shoulder_hip = [lshoulder_coord[0]-lhip_coord[0], lshoulder_coord[1]-lhip_coord[1]]
        rvec_shoulder_hip = [rshoulder_coord[0]-rhip_coord[0], rshoulder_coord[1]-rhip_coord[1]]
        lvec_knee_ankle = [lknee_coord[0]-lankle_coord[0], lknee_coord[1]-lankle_coord[1]]
        rvec_knee_ankle = [rknee_coord[0]-rankle_coord[0], rknee_coord[1]-rankle_coord[1]]


    #applying dot product formula
    #product of vectors
        lproductv = lvec_shoulder_hip[0]*lvec_knee_ankle[0] + lvec_shoulder_hip[1]*lvec_knee_ankle[1]
        rproductv = rvec_shoulder_hip[0]*rvec_knee_ankle[0] + rvec_shoulder_hip[1]*rvec_knee_ankle[1]

    #product of magnitudes
    #calculating magnitudes

        maglvec_hip_knee = math.sqrt(lvec_shoulder_hip[0]**2 + lvec_shoulder_hip[1]**2)
        magrvec_hip_knee = math.sqrt(rvec_shoulder_hip[0]**2 + rvec_shoulder_hip[1]**2)
        maglvec_knee_ankle = math.sqrt(lvec_knee_ankle[0]**2 + lvec_knee_ankle[1]**2)
        magrvec_knee_ankle = math.sqrt(rvec_knee_ankle[0]**2 + rvec_knee_ankle[1]**2)

        l_multmag = maglvec_hip_knee*maglvec_knee_ankle
        r_multmag = magrvec_hip_knee*magrvec_knee_ankle


        l_dotproduct = lproductv/l_multmag
        r_dotproduct = rproductv/r_multmag
    #finding angle inverse cosine
        l_radangle = math.acos(l_dotproduct)
        r_radangle = math.acos(r_dotproduct)

        l_degangle = 180-math.degrees(l_radangle)
        r_degangle = 180-math.degrees(r_radangle)
        
        
        
        if 0 < (l_degangle) < 160 or 0 < (r_degangle) < 160:
            text1 = cv.putText(frame, "Flatter!", (w-350,h-50), cv.FONT_HERSHEY_PLAIN, 3, (0,0,255), 4)
            print ("Flatter!")
        if 160 < (l_degangle) < 190 or 160 > (r_degangle) < 190:            
            text2 = cv.putText(frame, "Nice!", (w-350,h-50), cv.FONT_HERSHEY_PLAIN, 3, (0,255,0), 4)
            print ("NIce")
        

    
    
    
    cv.imshow('Video', frame)

    k = cv.waitKey(10) & 0xFF
    if k == ord('q'):
        break
cap.release()
cv.destroyAllWindows()