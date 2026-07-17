import bcrypt
from jinja2 import Environment, FileSystemLoader
from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps, globalps
from app.helper.authfunctions import authfnct
from app.helper.generalfunctions import getHostName
from app.helper.notificationfunction import sendEmail
from app.dbfunctions.userfunctions import getUserDataFromDB
from app.dbfunctions.workspacefunctions import getWorkspaceActiveURL
from app.dbfunctions.userfunctions import insertUpdateUserData
from app.properties.notificationproperties import notifyps
from app.dbfunctions.logfunctions import saveErrorLogtoDB

def doLogin(email: str, password: str):
    try:
        userps.email.set(email) # Set Email To Property
        user = getUserDataFromDB() # Execute Function to User Get Data
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
    except Exception as e:
        saveErrorLogtoDB("Auth", "", "doLogin", str(e))
        raiseAPIError(str(e), 500)

def validateJWT(token: str):
    payload = authfnct.verifyJWTToken(token)
    if not payload["status"]: # if Token is Invalid or expired
        return raiseInvalidError(payload["message"], 401)
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "Valid Token.",
            "payload": payload
        }
    )

def forgotPassword(email: str):
    try:
        userps.email.set(email) # Set Email To Property
        user = getUserDataFromDB() # Get User Data
        if user in (None, "", 0):
            return raiseInvalidError("Invalid email, Please enter register email id.", 401)
        jwt_token = authfnct.createFPJWTToken(user.id, user.email)
        env = Environment(loader=FileSystemLoader("app/assets/emailtemplate"))
        template = env.get_template("forgotpass.html")
        if globalps.IS_LOCAL_DEV == "1":
            reset_url = f"http://localhost:5173/resetpassword/{jwt_token}"
        else:
            reset_url = f"https://auth.{globalps.APP_DOMAIN}/resetpassword/{jwt_token}"
        html_body = template.render(
            name=f"{user.first_name} {user.last_name}",
            email=user.email,
            reset_url=reset_url
        )
        notifyps.to_email.set(user.email)
        notifyps.subject.set("Miidata : Forgot Password")
        notifyps.html.set(html_body)
        notifyps.bcc.set("miidata@genotypingaustralia.com.au")
        notifyps.attachments.set([])
        sendEmail(notifyps)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "A password reset link has been sent to your email address.",
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Auth", "", "forgotPassword", str(e))
        raiseAPIError(str(e), 500)

def resetPassword(token: str, password: str):
    try:
        result = authfnct.verifyJWTToken(token) # Verify Token
        if not result["status"]: # if Token is Invalid or expired
            return raiseInvalidError(result["message"], 401)
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user_id = result["payload"]["user_id"]
        userps.user_id.set(user_id)
        userps.db_upd_vals.set({"password": password.decode()})
        insertUpdateUserData() # Update Password in DB
        return JSONResponse(
            status_code=200,
            content={
                "status": True,
                "message": "Password reset successfully."
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Auth", "", "resetPassword", str(e))
        raiseAPIError(str(e), 500)