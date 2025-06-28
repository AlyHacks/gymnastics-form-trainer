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
         
        h = frame.shape[0]
        w = frame.shape[1]
        #create specific landmarks
        rshoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        lshoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        relbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
        lelbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        rwrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        lwrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]


        #get coordinates of landmarks
        rshouldercoord = (int(rshoulder.x*w), int(rshoulder.y*h))
        lshouldercoord = (int(lshoulder.x*w), int(lshoulder.y*h))
        relbowcoord = (int(relbow.x*w), int(relbow.y*h))
        lelbowcoord = (int(lelbow.x*w), int(lelbow.y*h))
        rwristcoord = (int(rwrist.x*w), int(rwrist.y*h))
        lwristcoord = (int(lwrist.x*w), int(lwrist.y*h))

        #create vectors

        rvec_shoulder_elbow = [rshouldercoord[0]-relbowcoord[0], rshouldercoord[1]-relbowcoord[1]]
        lvec_shoulder_elbow = [lshouldercoord[0]-lelbowcoord[0], lshouldercoord[1]-lelbowcoord[1]]                                            
        rvec_elbow_wrist = [relbowcoord[0]-rwristcoord[0], relbowcoord[1]-rwristcoord[1]]
        lvec_elbow_wrist = [lelbowcoord[0]-lwristcoord[0], lelbowcoord[1]-lwristcoord[1]]
        
        #magnitude of vectors

        mag_rvec_shoulder_elbow = math.sqrt(rvec_shoulder_elbow[0]**2 + rvec_shoulder_elbow[1]**2)
        mag_lvec_shoulder_elbow = math.sqrt(lvec_shoulder_elbow[0]**2 + lvec_shoulder_elbow[1]**2)
        mag_rvec_elbow_wrist = math.sqrt(rvec_elbow_wrist[0]**2 + rvec_elbow_wrist[1]**2)
        mag_lvec_elbow_wrist = math.sqrt(lvec_elbow_wrist[0]**2 + lvec_elbow_wrist[1]**2)

        lmultmag = mag_lvec_shoulder_elbow*mag_lvec_elbow_wrist
        rmultmag = mag_rvec_shoulder_elbow*mag_rvec_elbow_wrist

        #product of vectors
        lproduct = lvec_shoulder_elbow[0]*lvec_elbow_wrist[0] + lvec_shoulder_elbow[1]*lvec_elbow_wrist[1]
        rproduct = rvec_shoulder_elbow[0]*rvec_elbow_wrist[0] + rvec_shoulder_elbow[1]*rvec_elbow_wrist[1]

        #ddot product

        ldotproduct = lproduct/lmultmag
        rdotprodcut = rproduct/rmultmag

        lradangle = math.acos(ldotproduct)
        rradangle = math.acos(rdotprodcut)
        ldegangle = 180-math.degrees(lradangle)
        rdegangle = 180-math.degrees(rradangle)

        if 100 < (ldegangle) < 150 or 100 < (rdegangle) < 150:
            cv.putText(frame, "Push up, Lower!", (w-350, h-50), cv.FONT_HERSHEY_PLAIN, 3, (0,0,255), 4)
        elif 0 < (ldegangle) < 100  or 0 < (rdegangle) < 100:
            cv.putText(frame, "Nice!", (w-350, h-50), cv.FONT_HERSHEY_PLAIN, 3, (0,255,0), 4)

    cv.imshow('Video', frame)

    k = cv.waitKey(10) & 0xFF
    if k == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
