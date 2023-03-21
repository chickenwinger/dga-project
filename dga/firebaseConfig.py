import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

firebaseConfig = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': "management-transformer.firebaseapp.com",
    'databaseURL': "https://management-transformer-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "management-transformer",
    'storageBucket': "management-transformer.appspot.com",
    'messagingSenderId': "26656610083",
    'appId': "1:26656610083:web:b0f3e1aa42ed6437781e96",
    'measurementId': "G-PX46R86W7N"
}

firebase = pyrebase.initialize_app(firebaseConfig)
