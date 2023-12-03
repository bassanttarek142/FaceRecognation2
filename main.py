import os
import cv2

# Setup webcam
video = cv2.VideoCapture(0)
video.set(3, 765)
video.set(4,432)
# Read the background image
Background = cv2.imread('Resources/Background-01.png')
folderMode = 'Resources/Modes'
img_mode_path = os.listdir(folderMode)
img_mode_list = []
# Importing the mode Images in the Background
for path in img_mode_path:
 img_mode_list.append(cv2.imread(os.path.join(folderMode,path)))
while True:
 is_capture, frame = video.read()
 frame = cv2.resize(frame, (765, 432))
 Background[200:200 + 432, 55:55 + 765] = frame
 Background[140:140+ 420, 970:970 + 230] =img_mode_list[2]


 cv2.imshow("Attendace system", Background)
 press = cv2.waitKey(1)
 if press == ord("B"):
  break

video.release()
cv2.destroyAllWindows()