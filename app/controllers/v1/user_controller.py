from fastapi import  HTTPException
from sqlalchemy import select

from app.database.db_helper import get_table
from app.database.execute_stmt import execute_stmt
from app.database.execute_query import execute_query

from app.functions.authfunctions import create_token, verify_token
from app.services.firebase_service import send_push
from app.properties.usersproperties import usrproperties

import bcrypt

def login(email: str, password: str):

    users = get_table("users", "systemconfig")

    stmt = (
        select(users)
        .where(users.c.email == email)
    )

    user = execute_stmt(stmt, "one")

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
        "usrproperties.user_id": usrproperties.user_id,
        "usrproperties.first_name": usrproperties.first_name,
        "usrproperties.last_name": usrproperties.last_name,
        "itm_list": [user],
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
