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
    
    
        l_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        r_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
        l_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
        r_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]

        h = frame.shape[0]
        w = frame.shape[1]

        lhip_coord = (int(l_hip.x*w), int(l_hip.y*h))
        rhip_coord = (int(r_hip.x*w), int(r_hip.y*h))
        lknee_coord = (int(l_knee.x*w), int(l_knee.y*h))
        rknee_coord = (int(r_knee.x*w), int(r_knee.y*h))
        lankle_coord = (int(l_ankle.x*w), int(l_ankle.y*h))
        rankle_coord = (int(r_ankle.x*w), int(r_ankle.y*h))

    #vector time

        lvec_hip_knee = [lhip_coord[0]-lknee_coord[0], lhip_coord[1]-lknee_coord[1]]
        rvec_hip_knee = [rhip_coord[0]-rknee_coord[0], rhip_coord[1]-rknee_coord[1]]
        lvec_knee_ankle = [lknee_coord[0]-lankle_coord[0], lknee_coord[1]-lankle_coord[1]]
        rvec_knee_ankle = [rknee_coord[0]-rankle_coord[0], rknee_coord[1]-rankle_coord[1]]


    #applying dot product formula
    #product of vectors
        lproductv = lvec_hip_knee[0]*lvec_knee_ankle[0] + lvec_hip_knee[1]*lvec_knee_ankle[1]
        rproductv = rvec_hip_knee[0]*rvec_knee_ankle[0] + rvec_hip_knee[1]*rvec_knee_ankle[1]

    #product of magnitudes
    #calculating magnitudes

        maglvec_hip_knee = math.sqrt(lvec_hip_knee[0]**2 + lvec_hip_knee[1]**2)
        magrvec_hip_knee = math.sqrt(rvec_hip_knee[0]**2 + rvec_hip_knee[1]**2)
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
        
        
        if 50 < (l_degangle) < 100 or 50< (r_degangle) < 100:
            cv.putText(frame, "Squat lower!", (w-600,h-50), cv.FONT_HERSHEY_PLAIN, 3, (0,0,255), 4)
        if 0 < (l_degangle) < 50 or 0 < (r_degangle) < 50:            
            cv.putText(frame, "Nice!", (w-450,h-50), cv.FONT_HERSHEY_PLAIN, 3, (0,255,0), 4)
        
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
            cv.putText(frame, "Push up Lower!", (w-600, h-50), cv.FONT_HERSHEY_PLAIN, 3, (0,0,255), 4)
        elif 0 < (ldegangle) < 100  or 0 < (rdegangle) < 100:
            cv.putText(frame, "Nice!", (w-450, h-50), cv.FONT_HERSHEY_PLAIN, 3, (0,255,0), 4)
    
    
    
    cv.imshow('Video', frame)

    k = cv.waitKey(10) & 0xFF
    if k == ord('q'):
        break
cap.release()
cv.destroyAllWindows()