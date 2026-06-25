from fastapi import  Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.models import User
from app.functions.authfunctions import create_token, verify_token
import bcrypt
from app.services.firebase_service import send_push

from app.properties.usersproperties import usrproperties

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

    usrproperties.user_id = user_data.id
    usrproperties.first_name = user_data.first_name
    usrproperties.last_name = user_data.last_name
    usrproperties.user_array = [user_data]
    usrproperties.user_json = user_data
    
    return {
        "fetch_flag":"1",
        "access_token": access_token,
        "itm_list": [user_data],
        "usrproperties.user_id": usrproperties.user_id,
        "usrproperties.first_name": usrproperties.first_name,
        "usrproperties.last_name": usrproperties.last_name,
        "usrproperties.user_array": usrproperties.user_array,
        "usrproperties.user_json": usrproperties.user_json,
    }

def check_token(token: str):
    result = verify_token(token)
    return result

def test_push(token: str):
    response = send_push(
        token=token,
        title="Test Notification",
        body="Hello from Python"
    )
    return { "firebase_response": response }
