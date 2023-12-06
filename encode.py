import os
import cv2
import face_recognition
import pickle
folderpath = 'Datasets'
pathlist = os.listdir(folderpath)
print(pathlist)
img_list = []
studIds=[]
# Importing the mode Images in the Background
for path in pathlist:
 img_list.append(cv2.imread(os.path.join(folderpath,path)))
 studIds.append(os.path.splitext(path)[0])
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