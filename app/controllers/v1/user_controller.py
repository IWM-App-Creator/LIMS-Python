from fastapi import  HTTPException
from sqlalchemy import select

from app.database.db_helper import get_table
from app.database.execute_stmt import execute_stmt
from app.database.execute_query import execute_query

from app.functions.authfunctions import createJWTToken
from app.services.firebase.firebase_service import send_push
from app.properties.usersproperties import userps

import bcrypt

def login(email: str, password: str):

    users = get_table("users", "systemconfig")
    # print("users table:", users)
    stmt = (
        select(users)
        .where(users.c.email == email)
    )
    user = execute_stmt(stmt, "one") # Executed Query to get user data from database
    # Condition to check if data found or not found
    if not user:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid Email"
        )
    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        raise HTTPException(
            status_code = 401,
            detail = "Invalid Password"
        )

    access_token = createJWTToken(user.id, user.email) # JWT Token Generation for user pass param that we want to use in payload.

    # Set User Properties for API Response
    userps.user_id = user.id
    userps.first_name = user.first_name
    userps.last_name = user.last_name
    userps.user_array = [user]
    userps.user_json = user

    # Return API Response with JWT Token and User Data
    return {
        "fetch_flag": "1",
        "access_token": access_token,
        "user_id": userps.user_id,
        "first_name": userps.first_name,
        "last_name": userps.last_name,
        "itm_list": [user],
    }

# def check_token(token: str): # Validate JWT Token and return user data if valid, else return error message
#     result = verify_token(token)
#     return result

def test_push(token: str):
    response = send_push (
        token = token,
        title = "Test Notification",
        body = "Hello from Python"
    )
    return { "firebase_response": response }
