from fastapi import  Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.database import get_db, engine
from app.services.dynamic_table import get_table
from app.functions.authfunctions import create_token, verify_token
from app.services.firebase_service import send_push
from app.properties.usersproperties import usrproperties
from app.services.query_service import execute_query

import bcrypt

def login( email: str, password: str, db: Session = Depends(get_db)):

    users = get_table(engine,"users","systemconfig")

    stmt = (
        select(users)
        .where(users.c.email == email)
    )

    user = db.execute(stmt).mappings().first()

    # qry = """
    # SELECT 
    #     users.*
    # FROM users
    # WHERE users.email = :email
    # """
    # user = execute_query(
    #     db,
    #     qry,
    #     {"email": email}
    # )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    access_token = create_token(user.id, user.email)

    usrproperties.user_id = user.id
    usrproperties.first_name = user.first_name
    usrproperties.last_name = user.last_name
    usrproperties.user_array = [user]
    usrproperties.user_json = user

    return {
        "fetch_flag": "1",
        "access_token": access_token,
        "itm_list": [user],
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
