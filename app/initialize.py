from app.services.firebase.firebase_service import init_firebase

def initialize():
    init_firebase()
    print("Firebase initialized")
    