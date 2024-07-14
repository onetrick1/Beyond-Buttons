import cv2
import mediapipe as mp
import pyautogui
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


            # line_length = int(math.sqrt((half_frame_w - frame_x)**2 + (half_frame_h - frame_y)**2))
            # acceleration = 1
            # if line_length > circle_radius:
            #     acceleration = line_length - circle_radius

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
            #left_vert = abs(landmarks[145].y - landmarks[149].y)
            # right_horz = abs(landmarks[362].x - landmarks[263].x)
            # right_vert = abs(landmarks[386].y - landmarks[374].y)
            #left_horz = abs(landmarks[173].x - landmarks[33].x)
            
            # right_ratio = int((right_vert/right_horz)*100)
            #left_ratio = int((left_vert/left_horz)*10)

            ####LEFT EYE####
            left_eye = [landmarks[145], landmarks[159]] #landmarks[173], landmarks[33]]
            # for landmark in left_eye:
                # left_x = int(landmark.x * frame_w)
                # left_y = int(landmark.y * frame_h)
                # cv2.circle(frame, (left_x, left_y), 2, (0, 255, 0))

            if abs(left_eye[0].y - left_eye[1].y)*100 < 0.35:
                if startedL == False:
                    startedL = True
                    pyautogui.mouseDown()
            else:
                if startedL == True:
                    pyautogui.mouseUp()
                    startedL = False


            ####RIGHT EYE####
            right = [landmarks[374], landmarks[386]]
            # for landmark2 in right:
            #     right_x = int(landmark2.x * frame_w)
            #     right_y = int(landmark2.y * frame_h)
            #     cv2.circle(frame, (right_x, right_y), 2, (0, 255, 255))
            
            if abs(right[0].y - right[1].y)*100 < 0.35:
                pyautogui.click(button='right')
                pyautogui.sleep(0.2)


            #########SCREEN SHOTTING######
            ##############################
            if (abs(left_eye[0].y - left_eye[1].y)*100 < 0.35) and (abs(right[0].y - right[1].y)*100 < 0.35):
                print("screen")
                im1 = pyautogui.screenshot('my_screenshot.png')


            ########SCROLLING MODE#########
            ###############################
            lips = [landmarks[0], landmarks[17]]
            # for landmark3 in lips:
            #     lips_x = int(landmark3.x * frame_w)
            #     lips_y = int(landmark3.y * frame_h)
            #     cv2.circle(frame, (lips_x, lips_y), 2, (0, 255, 255))
            
            # print(lips[1].y - lips[0].y) #-0.125
            if lips[0].y - lips[1].y < -0.125:
                if SCROLL_MODE == False:
                    SCROLL_MODE = True
                    notifications.display(True)
                    pyautogui.sleep(1)
                else:
                    SCROLL_MODE = False
                    notifications.display(False)
                    pyautogui.sleep(1)
            

        if cv2.waitKey(1) == ord('q'):
            break

        cv2.imshow('Face Controlled Cursor', frame)
        cv2.waitKey(1)

    cam.release()
    cv2.destroyAllWindows()

cursor(1, 1)