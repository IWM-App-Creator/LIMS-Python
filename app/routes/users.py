from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth import create_token, verify_token
import bcrypt
from firebase_admin import messaging
from app.firebase_service import send_push

router = APIRouter()

@router.get("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Email")

    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="Invalid Password")

    access_token = create_token(user.id, user.email)

    user_data = {
        column.name: getattr(user, column.name)
        for column in user.__table__.columns
    }

    return {
        "fetch_flag":"1",
        "access_token": access_token,
        "itm_list": [user_data]
    }

@router.get("/check-token")
def check_token(token: str):
    result = verify_token(token)
    return result

@router.get("/test-notification")
def test_push(token: str):
    response = send_push(
        token=token,
        title="Test Notification",
        body="Hello from Python"
    )
    return { "firebase_response": response }
