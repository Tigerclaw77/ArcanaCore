import cv2
from intake.face_detect import extract_landmarks

img = cv2.imread("test.jpg")
landmarks = extract_landmarks(img)
print(len(landmarks))  # should be 468
print(landmarks[33], landmarks[263])  # eye landmarks
