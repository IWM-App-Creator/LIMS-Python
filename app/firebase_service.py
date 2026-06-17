import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from pathlib import Path


firebase_app = None

def init_firebase():
    global firebase_app
    if not firebase_admin._apps:
        service_account = (Path(__file__).resolve().parent/ "serviceAccountKey.json")
        cred = credentials.Certificate(str(service_account))
        firebase_app = firebase_admin.initialize_app(cred)
    return firebase_app

# def init_firebase():
#     if not firebase_admin._apps:
#         service_account = (Path(__file__).resolve().parent/ "serviceAccountKey.json")
#         cred = credentials.Certificate(str(service_account))
#         firebase_admin.initialize_app(cred)

def send_push(token: str, title: str, body: str):
    message = messaging.Message(
        token=token,
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
    )
    return messaging.send(message)