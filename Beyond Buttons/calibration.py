import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import matplotlib.pyplot as plt
from tkinter import *

font = cv2.FONT_HERSHEY_SIMPLEX 
fontScale = 1
color = (255, 0, 0) 
thickness = 2


def start():
    window = Tk()
    Button(window, text="Click When Ready For Calibration", command=window.destroy).pack() 
    window.mainloop()

def draw_square(top_left):
    top_right = top_left[0]+40, top_left[1]
    bottom_left = top_left[0], top_left[1]-40
    bottom_right = top_left[0]+40, top_left[1]-40

    return bottom_right

def isInside(circle_x, circle_y, rad, x, y):
    if ((x - circle_x)**2 + (y - circle_y)**2 <= rad**2):
        return True
    else:
        return False

def mouth():
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

    mouth = []
    time1 = []
    for t in range(100):
        time1.append(t)

    for a in range(100):
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape


        if a == 15 or a == 45 or a == 75:
            cv2.putText(frame, 'Open Mouth', (int(frame_w/2), int(frame_h/2)), font, fontScale, color, thickness)  

        if landmark_points:
            landmarks = landmark_points[0].landmark
            vert = abs(landmarks[0].y - landmarks[17].y)
            horz = abs(landmarks[57].x - landmarks[287].x)

            ratio = int((vert/horz)*10)

            lips = [landmarks[0], landmarks[17]]
            for landmark3 in lips:
                lips_x = int(landmark3.x * frame_w)
                lips_y = int(landmark3.y * frame_h)
                cv2.circle(frame, (lips_x, lips_y), 2, (0, 255, 255))

            mouth.append(ratio)

            time.sleep(0.1)

        cv2.imshow('Mouth Calibration', frame)
        cv2.waitKey(1)

    cam.release()
    cv2.destroyAllWindows()
    return mouth

def eye_ratio():
    """Calculate the Eye Aspect Ratio (EAR) to detect blink."""
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

    right, left = [], []

    for a in range(100):
        #####instructing users to blink at certain times

        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape
            

        if a == 15 or a == 45 or a == 75:
            cv2.putText(frame, 'BLINK', (int(frame_w/2), int(frame_h/2)), font, fontScale, color, thickness) 
       
        if landmark_points:
            landmarks = landmark_points[0].landmark
            right_vert = abs(landmarks[386].y - landmarks[374].y)
            left_horz = abs(landmarks[133].x - landmarks[33].x)
            left_vert = abs(landmarks[145].y - landmarks[159].y)
            right_horz = abs(landmarks[362].x - landmarks[263].x)
            
            right_ratio = int((right_vert/right_horz)*100)
            left_ratio = int((left_vert/left_horz)*100)

            left_eye = [landmarks[145], landmarks[159]] #landmarks[173], landmarks[33]]
            for landmark in left_eye:
                left_x = int(landmark.x * frame_w)
                left_y = int(landmark.y * frame_h)
                cv2.circle(frame, (left_x, left_y), 2, (0, 255, 0))

            right_eye = [landmarks[374], landmarks[386]]
            for landmark2 in right_eye:
                right_x = int(landmark2.x * frame_w)
                right_y = int(landmark2.y * frame_h)
                cv2.circle(frame, (right_x, right_y), 2, (0, 255, 255))

            right.append(right_ratio)
            left.append(left_ratio)

            time.sleep(0.1)

        cv2.imshow('Eye Calibration', frame)
        cv2.waitKey(1)

    cam.release()
    cv2.destroyAllWindows()
    return left, right

def nose_position():
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()
    half_screen_w, half_screen_h = int(screen_w/2), int(screen_h/2)

    circle_radius = 20

    frame_w = 640
    frame_h = 480
    half_frame_w, half_frame_h = frame_w/2, frame_h/2
    DFEX, DFEY = int(frame_w/8), int(frame_h/8)

    CENTER = False
    BL = False
    BR = False
    TL = False
    TR = False


    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks

        frame_h, frame_w, _ = frame.shape
        half_frame_w, half_frame_h = int(frame_w/2), int(frame_h/2)

        cv2.circle(frame, (half_frame_w, half_frame_h), circle_radius, (0, 255, 0), -1) #center of screen
        cv2.circle(frame, (DFEX, DFEY), circle_radius, (0, 255, 0), -1) #bottom left
        cv2.circle(frame, (frame_w-DFEX, DFEY), circle_radius, (0, 255, 0), -1) #bottom right
        cv2.circle(frame, (DFEX, frame_h-DFEY), circle_radius, (0, 255, 0), -1) #top left
        cv2.circle(frame, (frame_w-DFEX, frame_h-DFEY), circle_radius, (0, 255, 0), -1) #top right

        if CENTER == True:
            cv2.putText(frame, 'DONE', (int(half_frame_w), int(half_frame_h)), font, fontScale, color, thickness)
        if BL == True:
            cv2.putText(frame, 'DONE', (int(DFEX), int(DFEY)), font, fontScale, color, thickness)
        if BR == True:
            cv2.putText(frame, 'DONE', (int(frame_w-DFEX), int(DFEY)), font, fontScale, color, thickness)
        if TL == True:
            cv2.putText(frame, 'DONE', (int(DFEX), int(frame_h-DFEY)), font, fontScale, color, thickness)
        if TR == True:
            cv2.putText(frame, 'DONE', (int(frame_w-DFEX), int(frame_h-DFEY)), font, fontScale, color, thickness)


        if landmark_points:
            landmarks = landmark_points[0].landmark
            nose_position = landmarks[4] #4 is tip of nose
            screen_x = int(nose_position.x * screen_w)
            screen_y = int(nose_position.y * screen_h)
            frame_x = int(nose_position.x * frame_w)
            frame_y = int(nose_position.y * frame_h)

            cv2.circle(frame, (frame_x, frame_y), 2, (0, 255, 0), -1) #center of nose

            if(isInside(half_frame_w, half_frame_h, circle_radius, frame_x, frame_y)):
                CENTER = True
            if(isInside(DFEX, DFEY, circle_radius, frame_x, frame_y)):
                BL = True
            if(isInside(frame_w-DFEX, DFEY, circle_radius, frame_x, frame_y)):
                BR = True
            if(isInside(DFEX, frame_h-DFEY, circle_radius, frame_x, frame_y)):
                TL = True
            if(isInside(frame_w-DFEX, frame_h-DFEY, circle_radius, frame_x, frame_y)):
                TR = True

        cv2.imshow(':D', frame)
        cv2.waitKey(1)

        if CENTER and BL and BR and TL and TR:
            cam.release()
            cv2.destroyAllWindows()
            return True

def calibrate():
    start()
    mouth_data = mouth()
    left_eye, right_eye = eye_ratio()
    #nose_position()
    return mouth_data, left_eye, right_eye

