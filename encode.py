import os
import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': "facerecognition-159b3.appspot.com"
})

folderpath = 'Datasets'
pathlist = os.listdir(folderpath)
print(pathlist)
img_list = []
studIds = []

# Upload images to Firebase Storage and store their paths
for path in pathlist:
    img_list.append(cv2.imread(os.path.join(folderpath, path)))
    studIds.append(os.path.splitext(path)[0])

    fileName = f'{folderpath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)

    try:
        blob.upload_from_filename(fileName)
        print(f"File {fileName} uploaded successfully.")
    except Exception as e:
        print(f"Error uploading file {fileName}: {str(e)}")
        # Implement retry logic or handle the error as needed

print(studIds)


# Function to find face encodings
def find_encode(image_list):
    encode_list = []
    for img in image_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list


print("Encoding started")
encode_list_known = find_encode(img_list)
encode_list_with_ids = [encode_list_known, studIds]
print(encode_list_known)
print("Encoding completed")

# Save the encodings to a file using Pickle
file = open("Encodingfile.p", "wb")
pickle.dump(encode_list_with_ids, file)
file.close()
print("Encodings saved to file")

