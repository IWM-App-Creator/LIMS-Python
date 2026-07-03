import bcrypt
from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, globalps
from app.functions.authfunctions import authfnct
from app.functions.generalfunctions import getHostName

def doLogin(email: str, password: str):
    # print("doLogin --> ")
    # getHostName(request). # $domain_url = $GeneralFunctions->getDomainNameFromURL();
    # print("request_context --> ", globalps.req_subdomain)
    # $login_access = $GeneralFunctions->canUserLogin($user->role_id);
    # $is_valid_ws = $GeneralFunctions->isWorkSpaceURLValid($user->id);
    tbluser = DB.getTableMeta("users", "systemconfig").alias("usr")
    stmt = (
        select(tbluser).where(tbluser.c.email == email)
    )
    user = DB.executeDBSelectSingle(stmt)
    # print("user --> ", user.email)

    if not user:  # Invalid User
        raiseAPIError("Invalid Email", 401)

    if not bcrypt.checkpw(password.encode(), user.password.encode()): # Invalid Password
        raiseAPIError("Invalid Password", 401)

    # If Success Generate JWT Token
    access_token = authfnct.createJWTToken(user.id, user.role_id, user.email)

    # To Pass Menu, Dashboard List, Association
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "Login successful",
            "access_token": access_token,
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "user_settings": user.user_settings,
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