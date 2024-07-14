from tkinter.font import families
import cv2
import mediapipe as mp
import pyautogui
from pyscreeze import screenshot
import notifications
import time
import math

def isInside(circle_x, circle_y, rad, x, y):
    if ((x - circle_x)**2 + (y - circle_y)**2 <= rad**2):
        return True
    else:
        return False


def cursor(left_threshold, right_threshold):
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True) #to give the exact coordinates of landmarks
    screen_w, screen_h = pyautogui.size()
    half_screen_w, half_screen_h = int(screen_w/2), int(screen_h/2)
        

    circle_radius = 30
    acceleration = 8
    SCROLL_MODE = False
    startedL = False
    startedR = False
    screenstart = False
    mouseDownL = False
    mouseDownR = False

    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1) #flipping camera so it's accurate
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks

        frame_h, frame_w, _ = frame.shape
        half_frame_w, half_frame_h = int(frame_w/2), int(frame_h/2)

        cv2.circle(frame, (half_frame_w, half_frame_h), circle_radius, (0,0,255), 1)
        #cv2.circle(frame, (half_frame_w, half_frame_h), 4, (0,0,255), -1) say it's needed for calibration

        if landmark_points: #checking if a face is detected
            landmarks = landmark_points[0].landmark

            ########### ALL CURSOR MOVEMENT ##########
            ##########################################
            nose_position = landmarks[4] #4 is tip of nose
            screen_x = int(nose_position.x * screen_w)
            screen_y = int(nose_position.y * screen_h)
            frame_x = int(nose_position.x * frame_w)
            frame_y = int(nose_position.y * frame_h)

            cv2.circle(frame, (frame_x, frame_y), 2, (0, 255, 0), -1) #center of nose
            cv2.line(frame, (half_frame_w, half_frame_h), (frame_x, frame_y), (0, 255, 0))


            if(isInside(half_frame_w, half_frame_h, circle_radius, frame_x, frame_y)):
                pass
            else:
                diff_x = screen_x - half_screen_w
                diff_y = screen_y - half_screen_h
                if SCROLL_MODE == False: #checking if user is on scroll mode
                    pyautogui.move(diff_x/acceleration, diff_y/acceleration)
                else:
                    pyautogui.scroll(int(diff_y/acceleration))


            ##########CLICKS AND DRAGS##############
            ##############################
            right_vert = abs(landmarks[386].y - landmarks[374].y)
            left_horz = abs(landmarks[133].x - landmarks[33].x)
            left_vert = abs(landmarks[145].y - landmarks[159].y)
            right_horz = abs(landmarks[362].x - landmarks[263].x)

            right_ratio = int((right_vert/right_horz)*100)
            left_ratio = int((left_vert/left_horz)*100)
            
            if left_ratio < left_threshold:
                if startedL == False:
                    startedL = True

                    starttimeL = time.time()
                
                else:
                    laptimeL = round((time.time() - starttimeL), 2)
                    #print(laptime)
                    if laptimeL > 0.2 and mouseDownL == False:
                        pyautogui.mouseDown()
                        mouseDownL = True 
            else:
                if startedL == True:
                    pyautogui.mouseUp()
                    startedL = False
                    mouseDownL = False
            

            if right_ratio < right_threshold:
                if startedR == False:
                    startedR = True
                    starttimeR = time.time()
                else:
                    laptimeR = round((time.time() - starttimeR), 2)
                    if laptimeR > 0.3:
                        pyautogui.click(button='right')
                        pyautogui.sleep(0.2)
                        startedR = False
            
            else:
                startedR = False


            #########SCREEN SHOTTING######
            ##############################
            # if (left_ratio < left_threshold) and (right_ratio < right_threshold):
            #     if screenstart == False:
            #         screenstart = True
            #         screenstarttime = time.time()
            #     else:
            #         laptimescreen = round((time.time() - screenstarttime), 2)
            #         if laptimescreen > 0.8:
            #             print("screen")
            #             im1 = pyautogui.screenshot('my_screenshot.png')


            ########SCROLLING MODE#########
            ###############################
            vert = abs(landmarks[0].y - landmarks[17].y)
            horz = abs(landmarks[57].x - landmarks[287].x)
            mouth_ratio = int((vert/horz)*10)
            
            # print(lips[1].y - lips[0].y) #-0.125
            # if mouth_ratio > mouth_threshold:
            #     if SCROLL_MODE == False:
            #         SCROLL_MODE = True
            #         notifications.display(True)
            #         pyautogui.sleep(1)
            #     else:
            #         SCROLL_MODE = False
            #         notifications.display(False)
            #         pyautogui.sleep(1)
            

        if cv2.waitKey(1) == ord('q'):
            break

        cv2.imshow('Face Controlled Cursor', frame)
        cv2.waitKey(1)

    cam.release()
    cv2.destroyAllWindows()

cursor(10, 10)