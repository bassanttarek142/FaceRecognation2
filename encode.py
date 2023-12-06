import os
import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : "https://facerecognition-159b3-default-rtdb.firebaseio.com/",
    'storageBucket' : "facerecognition-159b3.appspot.com"
})

folderpath = 'Datasets'
pathlist = os.listdir(folderpath)
print(pathlist)
img_list = []
studIds=[]

for path in pathlist:
 img_list.append(cv2.imread(os.path.join(folderpath,path)))
 studIds.append(os.path.splitext(path)[0])
 
 fileName = f'{folderpath}/{path}'
 bucket = storage.bucket()
 blob = bucket.blob(fileName)
 blob.upload_from_filename(fileName)

print(studIds)

def findencode(imagelist):
    encodlist=[]
    for img in imagelist:
      img =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
      encode=face_recognition.face_encodings(img)[0]
      encodlist.append(encode)
    return encodlist

print("encoding start")

encodelistknown=findencode(img_list)
encodelistknownwithids=[encodelistknown,studIds]
print(encodelistknown)
print("encoding ends")
file=open("Encodingfile.p","wb")
pickle.dump(encodelistknownwithids,file)
file.close()
print("file saved")