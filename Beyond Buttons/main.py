import cv2
import mediapipe as mp
import pyautogui
import time
import math
import calibration
import cursor
import userSetting

mouth_data, left_eye, right_eye = calibration.calibrate() #returns the ratio of both eyes' vertical to horizontal distance
#returns a list of int(vertical/horizontal * 100) over the time of 10 seconds

left_threshold = int((max(left_eye) + min(left_eye))/2)
right_threshold = int((max(right_eye) + min(right_eye))/2)
mouth_threshold = int((max(mouth_data) + min(mouth_data))/2)

userSetting.display()
cursor.cursor(mouth_threshold, left_threshold, right_threshold)