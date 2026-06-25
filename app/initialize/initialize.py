from app.services.firebase_service import init_firebase

def initialize():
    init_firebase()
    print("Firebase initialized")
    