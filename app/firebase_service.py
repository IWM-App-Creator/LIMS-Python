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

def send_push(token: str, title: str, body: str):
    try:
        message = messaging.Message(
            token=token.strip(),
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data={
                "title":title,
                "body":body,
            }
        )

        response = messaging.send(message)
        return {"message_id": response}

    except messaging.UnregisteredError:
        print("❌ Token expired or invalid")
        # delete token from database
        return {"error": "invalid_token"}

    except messaging.SenderIdMismatchError:
        print("❌ Token belongs to another Firebase project")
        return {"error": "sender_id_mismatch"}

    except Exception as e:
        print("❌ FCM error:", repr(e))
        return {"error": str(e)}