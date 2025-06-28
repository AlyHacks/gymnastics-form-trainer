import cv2 as cv
import mediapipe as mp
import numpy as np

capture = cv.VideoCapture(1)
mp_pose =  mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose() #pose detection
while True:
    ret, frame = capture.read()
    if not ret:
        break
    
    resizeFrame = cv.resize(frame, (0,0), fx=0.5, fy=0.75)
    rgb_frame = cv.cvtColor(resizeFrame, cv.COLOR_BGR2RGB)

    
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    

    cv.imshow('Frame', frame)
    if cv.waitKey(10)& 0xFF == 27:
        break


