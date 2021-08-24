from django.shortcuts import render
import cv2
from .gaze_tracking import GazeTracking
import pandas as pd
import numpy as np
import os
import time

# Create your views here.
def headpose_estimation(request):
    """
    Demonstration of the GazeTracking library.
    """

    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    data_list = []

    fps = 0
    frame_counter = 0
    start_time = time.time()

    K = [6.2500000000000000e+002, 0.0, 3.1250000000000000e+002,
        0.0, 6.2500000000000000e+002, 3.1250000000000000e+002,
        0.0, 0.0, 1.0]

    # 3D model points.
    model_points = np.array([
       (0.0, 0.0, 0.0),  # Nose tip
       (0.0, -330.0, -65.0),  # Chin
       (-225.0, 170.0, -135.0),  # Left eye left corner
       (225.0, 170.0, -135.0),  # Right eye right corne
       (-150.0, -150.0, -125.0),  # Left Mouth corner
       (150.0, -150.0, -125.0)  # Right mouth corner

    ])


    while True:
       # We get a new frame from the webcam
       _, frame = webcam.read()
       size = frame.shape

       # We send this frame to GazeTracking to analyze it
       gaze.refresh(frame)

       frame = gaze.annotated_frame()
       text = ""

       if gaze.is_blinking():
           text = "Blinking"
       if gaze.is_right():
           text = "Looking right"
       elif gaze.is_left():
           text = "Looking left"
       elif gaze.is_center():
           text = "Looking center"
       os.system('espeak {0}'.format(text))

       h, w, c = frame.shape

       frame_counter +=1
       fps = (frame_counter /(time.time() - start_time))

       cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 0, 0), 2)
       # Display FPS and size of object
       cv2.putText(frame, 'FPS: {:.2f}'.format(fps), (20, 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 255),2)

       left_pupil = gaze.pupil_left_coords()
       right_pupil = gaze.pupil_right_coords()

       if left_pupil is not None and right_pupil is not None:
           # first_quad = [(597, 150), (702, 200)]  # Top-left, Bottom right - 1st quad
           # first_quad = [(0, 150), (600, 200)]  # Top-right, Bottom right - 1st quad

           center_x = int((left_pupil[0] + right_pupil[0]) / 2)
           center_y = int((left_pupil[1] + right_pupil[1]) / 2)

           # Camera internals
           focal_length = size[1]
           center = (size[1] / 2, size[0] / 2)
           cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)

           # We are then accesing the landmark points
           i = [33, 8, 36, 45, 48,
                54]  # Nose tip, Chin, Left eye corner, Right eye corner, Left mouth corner, right mouth corner
           image_points = []
           for n in i:
               x = gaze.gaze_landmarks.part(n).x
               y = gaze.gaze_landmarks.part(n).y
               # image_points = np.array([(x,y)], dtype="double")
               image_points += [(x, y)]
               cv2.circle(frame, (x, y), 2, (255, 255, 0), -1)

           image_points = np.array(image_points, dtype="double")
           # print(image_points)
           print("Camera Matrix :\n {0}".format(cam_matrix))

           dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
           (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points,
                                                                         cam_matrix, dist_coeffs,
                                                                         flags=cv2.SOLVEPNP_ITERATIVE)

           print("Rotation Vector:\n {0}".format(rotation_vector))
           print("Translation Vector:\n {0}".format(translation_vector))

           # Project a 3D point (0, 0, 1000.0) onto the image plane.
           # We use this to draw a line sticking out of the nose

           (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
               translation_vector,
               cam_matrix, dist_coeffs)
    #This is for accessing the quadrant
           for p in image_points:
               cv2.circle(frame, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

           p1 = (int(image_points[0][0]), int(image_points[0][1]))
           p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
           center_nose_x = image_points[0][0]
           center_nose_y = image_points[0][1]
           end_nose_x = nose_end_point2D[0][0][0]
           end_nose_y = nose_end_point2D[0][0][1]


           cv2.line(frame, (0, int(center_nose_y)), (w, int(center_nose_y)), (0, 255, 0), 2)
           cv2.line(frame, (int(center_nose_x), 0), (int(center_nose_x), h), (0, 255, 0), 2)
           cv2.line(frame, p1, p2, (255, 0, 0), 2)
           cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
           cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)

           cv2.imshow("Head Pose Estimation", frame)


           if cv2.waitKey(1) == 27:
               break

    #This is for taking data if it is necessary
    df = pd.DataFrame(data_list, columns=['left_pupil','right_pupil','gaze_center_x', 'gaze_center_y', 'nose_end_points',
    'gaze_end_points'])
    df.to_csv("myrecorded_data.csv")