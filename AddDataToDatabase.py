import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : "https://facerecognition-159b3-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "120200181" :
    {
        "name" : "Rowida Elsayed",
        "id" : "120200181",
        "total_attendance":6,
        "year" : 4,
        "Last_attendance_time" : "2023-12-07 00:54:34"
    },
     "120200013" :
    {
        "name" : "Rewan Yehia",
        "id" : "120200013",
        "total_attendance":6,
        "year" : 4,
        "Last_attendance_time" : "2023-12-07 00:54:34"
    },
     "120200244" :
    {
        "name" : "Bassant Tarek",
        "id" : "120200244",
        "total_attendance":6,
        "year" : 4,
        "Last_attendance_time" : "2023-12-07 00:54:34"
    },
     "120200211" :
    {
        "name" : "Noha Mahmoud",
        "id" : "120200211",
        "total_attendance":6,
        "year" : 4,
        "Last_attendance_time" : "2023-12-07 00:54:34"
    },
     "120200067" :
    {
        "name" : "Gasser Amr",
        "id" : "120200067",
        "total_attendance":6,
        "year" : 4,
        "Last_attendance_time" : "2023-12-07 00:54:34"
    },


}

for key, value in data.items():
    ref.child(key).set(value)