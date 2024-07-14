import cv2
import mediapipe as mp
import pyautogui
import time

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True) #to give the exact coordinates of landmarks
screen_w, screen_h = pyautogui.size()
screen_x = screen_w/2
screen_y = screen_h/2


def draw_square(top_left):
    top_right = top_left[0]+40, top_left[1]
    bottom_left = top_left[0], top_left[1]-40
    bottom_right = top_left[0]+40, top_left[1]-40

    return bottom_right


while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1) #flipping camera so it's accurate
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    half_screen_w = int(frame_w/2)
    half_screen_h = int(frame_h/2)

    left_top_left = half_screen_w-120, half_screen_h+40
    up_top_left = half_screen_w-20, half_screen_h+120
    right_top_left = half_screen_w+80, half_screen_h+40
    down_top_left = half_screen_w-20, half_screen_h-80
    
    cv2.rectangle(frame, left_top_left, draw_square(left_top_left), (0,255,0),3)
    cv2.rectangle(frame, up_top_left, draw_square(up_top_left), (0,255,0),3)
    cv2.rectangle(frame, right_top_left, draw_square(right_top_left), (0,255,0),3)
    cv2.rectangle(frame, down_top_left, draw_square(down_top_left), (0,255,0),3)


    if landmark_points:
        landmarks = landmark_points[0].landmark

        # eye_height = (landmarks[474].y  - landmarks[476].y) * frame_h#height
        # eye_width = (landmarks[475].x - landmarks[477].x) * frame_w #width
        # eye_center_x = eye_width / 2
        # eye_center_y = eye_height / 2
        # print(eye_center_x)
        # print(eye_center_x, eye_center_y)
        # eye_area = eye_height*eye_width/2
        # frame_eye_ratio = frame_area / eye_area

        landmark = landmarks[473] #473:478 are all right eye
        x = int(landmark.x * frame_w)
        y = int(landmark.y * frame_h)
        cv2.circle(frame, (x, y), 3, (0, 255, 0)) #right eye

        if (x > left_top_left[0]) and (x < draw_square(left_top_left)[0]) and (y < left_top_left[1]) and (y > draw_square(left_top_left)[1]):
            pyautogui.moveTo(screen_x, screen_y)
            screen_x -= 10
        if (x > up_top_left[0]) and (x < draw_square(up_top_left)[0]) and (y < up_top_left[1]) and (y > draw_square(up_top_left)[1]):
            pyautogui.moveTo(screen_x, screen_y)
            screen_y += 10
        if (x > right_top_left[0]) and (x < draw_square(right_top_left)[0]) and (y < right_top_left[1]) and (y > draw_square(right_top_left)[1]):
            pyautogui.moveTo(screen_x, screen_y)
            screen_x += 10        
        if (x > down_top_left[0]) and (x < draw_square(down_top_left)[0]) and (y < down_top_left[1]) and (y > draw_square(down_top_left)[1]):
            pyautogui.moveTo(screen_x, screen_y)
            screen_y -= 10


        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255)) #left eye
        if (left[0].y - left[1].y) < 0.004:
            pyautogui.click()
            pyautogui.sleep(1)

            
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)