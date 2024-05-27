import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("./firebasestorage/firebase_key.json")
firebase_admin.initialize_app(cred, {"storageBucket": "static-5d4d6.appspot.com"})

bucket = storage.bucket()
