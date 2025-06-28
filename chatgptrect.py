import cv2 as cv
import numpy as np
import mediapipe as mp

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

    cv.imshow('Video', frame)
    if cv.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()