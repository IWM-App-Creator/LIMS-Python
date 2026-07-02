from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.dbhelper.db_helper import DB
from app.httphelper.responsehelper import raiseAPIError
from app.functions.authfunctions import authfnct
from app.properties.globalproperties import globalps

import bcrypt

def doLogin(email: str, password: str):
    # print("doLogin email:", email)
    # print("doLogin password:", password)

    # $domain_url = $GeneralFunctions->getDomainNameFromURL();
    # $login_access = $GeneralFunctions->canUserLogin($user->role_id);
    # $is_valid_ws = $GeneralFunctions->isWorkSpaceURLValid($user->id);

    users = DB.getTableMeta("users", "systemconfig")
    print("users table:", users)
    tbluser = DB.getTableMeta("users", "systemconfig").alias("usr")
    stmt = (
        select(tbluser)
            .where(tbluser.c.email == email)
    )
    user = DB.executeDBSelectSingle(stmt)
    # print("user --> ", user.email)

    if not user:  # Invalid User
        raiseAPIError("Invalid Email", 401)

    if not bcrypt.checkpw(password.encode(), user.password.encode()): # Invalid Password
        raiseAPIError("Invalid Password", 401)

    # If Success Generate JWT Token
    access_token = authfnct.createJWTToken(user.id, user.email)
    globalps.user_id = user.id
    globalps.first_name = user.first_name
    globalps.last_name = user.last_name
    globalps.email = user.email
    globalps.user_settings = user.user_settings

    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "Login successful",
            "access_token": access_token,
            "user_id": globalps.user_id,
            "first_name": globalps.first_name,
            "last_name": globalps.last_name,
            "email": globalps.email,
            "user_settings": globalps.user_settings,
        }
    )

def validateJWT(token: str):
    # result = verify_token(token)
    result = authfnct.verifyJWTToken(token)
    return result

def forgotPassword(email: str):
    result = authfnct.verifyJWTToken(token)
    return result

def resetPassword(token: str, newpass: str, confirm_pass: str):
    result = authfnct.verifyJWTToken(token)
    return result