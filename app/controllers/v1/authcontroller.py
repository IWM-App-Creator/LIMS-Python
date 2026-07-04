import bcrypt
from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, userps
from app.functions.authfunctions import authfnct
from app.functions.generalfunctions import getHostName
from app.functions.userfunctions import getUserDataFromDB
from app.functions.workspacefunctions import getWorkspaceActiveURL

def doLogin(email: str, password: str):
    # print("doLogin --> ")
    # tbluser = DB.getTableMeta("users", "systemconfig").alias("usr")
    # stmt = (
    #     select(tbluser).where(tbluser.c.email == email)
    # )
    # user = DB.executeDBSelectSingle(stmt)
    userps.email.set(email) # Set Email To Property
    user = getUserDataFromDB()  # Execute Function to Get Data

    if not user: # Invalid User
        raiseAPIError("Invalid Email", 401)

    if not bcrypt.checkpw(password.encode(), user.password.encode()): # Invalid Password
        raiseAPIError("Invalid Password", 401)

    if user.role_id != 1 and user.role_id != 2 : # Check User Access
        raiseAPIError("Your don't have permission to login.", 401)

    # If Success Generate JWT Token
    access_token = authfnct.createJWTToken(user.id, user.role_id, user.email)
    # Get Active Workspace URL 
    userps.workspace_id.set(user.active_ws)
    active_ws_url = getWorkspaceActiveURL()
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "Login successful",
            "access_token": access_token,
            "redirect_url": active_ws_url,
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