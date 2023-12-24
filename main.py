import cv2
import pickle
import os
import face_recognition
import firebase_admin
import numpy as np
import cvzone

from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognition-159b3-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecognition-159b3.appspot.com"
})


def resize_image(img, target_size):
    return cv2.resize(img, target_size)


bucket = storage.bucket()
# Setup webcam
video = cv2.VideoCapture(0)
video.set(3, 765)
video.set(4, 432)

# Read the background image
Background = cv2.imread('Resources/Background-01.png')
folderMode = 'Resources/Modes'
img_mode_path = os.listdir(folderMode)
img_mode_list = []

# Importing the mode Images in the Background
for path in img_mode_path:
    img_mode_list.append(cv2.imread(os.path.join(folderMode, path)))

# Load the encoding file that has ids
print("Loading Encodingfile")
file = open("Encodingfile.p", "rb")
encodelistknownwithids = pickle.load(file)
file.close()
encodelistknown, studIds = encodelistknownwithids
print("Encodingfile loaded")

modetype = 0
counter = 0
student_id = -1
imgStudent = []

while True:
    is_capture, frame = video.read()
    frame_small = cv2.resize(frame, (765, 432), None, 0.25, 0.25)
    frame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)

    facecurframe = face_recognition.face_locations(frame_small)

    encodecurframe = face_recognition.face_encodings(frame_small, facecurframe)

    Background[200:200 + 432, 55:55 + 765] = frame_small
    Background[140:140 + 420, 970:970 + 230] = img_mode_list[modetype]

    # Compare between encoding generator match or not
    for encodeface, faceloc in zip(encodecurframe, facecurframe):
        matches = face_recognition.compare_faces(encodelistknown, encodeface)
        facedistance = face_recognition.face_distance(encodelistknown, encodeface)

        matchIndex = np.argmin(facedistance)  # give the index where the face is recognized

        if matches[matchIndex] == True:
            print("Detected Known Face")
            print(studIds[matchIndex])

            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 200 + y1, x2 - x1, y2 - y1

            #Background = cvzone.cornerRect(Background, bbox, rt=0)
            student_id = studIds[matchIndex]
            # Change the modes in the Background
            if counter == 0:
                counter = 1
                modetype = 1

    if counter != 0:
        # Get the studentInfo from the database based on his id
        if counter == 1:
            studentInfo = db.reference(f'Students/{student_id}').get()
            print(studentInfo)
        # Get the Image from the storage
        blob = bucket.get_blob(f'Datasets/{student_id}.png')
        print(f'Retrieving image with ID: {student_id}')

        blobs = bucket.list_blobs()
        array = np.frombuffer(blob.download_as_string(), np.uint8)
        imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

        # New target size for the student's image (width, height)
        target_size = (200, 200)

        # Resize the student's image
        imgStudent = resize_image(imgStudent, target_size)

        cv2.putText(Background, studentInfo['name'], (1046, 440),
                    cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 0, 0), 1)

        cv2.putText(Background, studentInfo['id'], (1050, 517),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 0, 0), 1)

        # Placement coordinates for the new size (adjust as needed)
        placement_start_x = 982
        placement_start_y = 140
        Background[placement_start_y:placement_start_y + target_size[1],
        placement_start_x:placement_start_x + target_size[0]] = imgStudent

        counter += 1

    cv2.imshow("Attendance system", Background)
    press = cv2.waitKey(1)
    if press == ord("B"):
        break

video.release()
cv2.destroyAllWindows()


