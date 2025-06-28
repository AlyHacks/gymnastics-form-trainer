An AI-powered gymnastics form trainer that tells the user to do specific actions to make it better. It uses a webcam to detect movement and to correct the skills in real time. It corrects push-ups, V-ups, hollow holds, squats, and handstands, which are all valuable to gymnastics conditioning. This is an easy at-home trainer for gymnasts.

Overview
--------
As a gymnast, I often struggled with conditioning outside of gymnastics practice. Without a coach at my side, I wasn’t able to do exercises correctly and do my workouts efficiently. I wasn’t able to do gymnastics exercises at home when I needed to train the most. So, a solution to this problem was to create a real-time pose detection model for evaluating my gymnastics exercises. Using OpenCV and Mediapipe, I was able to create an AI detection that tells users if their exercises were correct based on form. 

What it does
-----
The user can run the code, which will open a new window with visual landmarks on their bodies. Then, while the user does the exercise, the model will detect the angle between limbs and evaluate the correct form. By giving real-time feedback on the window (printing messages), the user can further correct the form and shape of the exercise.

Features
-----
Runs the default camera

Uses AI Mediapipe detection

Visual landmarks for the user

Message for user

Future Steps
------
I would like to implement more exercises into this detection system for a more versatile model that can evaluate even more gymnastics workouts. I would also like to include a UI, a GUI that allows the user to navigate this application more easily. 
