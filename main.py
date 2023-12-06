import cv2
import pickle
import os
import face_recognition
import numpy as np
#import cvzone
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
#load the encoding file that have ids
print("Loading Encodingfile")
file=open("Encodingfile.p","rb")
encodelistknownwithids=pickle.load(file)
file.close()
encodelistknown,studIds=encodelistknownwithids
print("Encodingfile loaded")
while True:
  is_capture, frame = video.read()
  frame_small = cv2.resize(frame, (765, 432),None,0.25,0.25)
  frame_small =cv2.cvtColor(frame_small,cv2.COLOR_BGR2RGB)
  facecurframe=face_recognition.face_locations(frame_small)
  encodecurframe=face_recognition.face_encodings(frame_small,facecurframe)
  Background[200:200 + 432, 55:55 + 765] = frame_small
  Background[140:140+ 420, 970:970 + 230] =img_mode_list[2]
  for encodeface,faceloc in zip(encodecurframe,facecurframe):
     matches=face_recognition.compare_faces(encodelistknown,encodeface)
     faceid=face_recognition.face_distance(encodelistknown,encodeface)
     matchIndex=np.argmin(faceid) #give the index where the face is recognized
     if matches[matchIndex]==True:
        print("Detected Known Face")
        y1,x2,y2,x1=faceloc
        y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
        bbox=55+x1,162+y1,x2-x1,y2-y1
        #imageBackground=cvzone.cornerRect(imageBackground,bbox,rt=0)
  cv2.imshow("Attendace system", Background)
  press = cv2.waitKey(1)
  if press == ord("B"):
    break

video.release()
cv2.destroyAllWindows()