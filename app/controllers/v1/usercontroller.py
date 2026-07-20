import json
import bcrypt
from app.utils.common import DB, select, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.dbfunctions.userfunctions import getUserDataFromDB, insertUpdateUserData
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.workspacefunctions import getUserWSData
from app.properties.dbproperties import dbps
from app.helper.generalfunctions import uploadFile, addUpdateJson, getWSUserRole
from app.helper.userhelper import setUserProperties
from app.helper.menuhelper import getUserMenuList
from app.helper.workspacehelper import getUserWSList
from app.helper.dashboardhelper import getUserDashboards
from app.properties.menuproperties import menups
from app.properties.workspaceproperties import wsps
from app.properties.dashboardproperties import dps

# http://xytovet.localhost:8000/api/v1/user/getdetail?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzc3OSIsInJvbGVfaWQiOiIxIiwiZW1haWwiOiJjaGludGFuaXQyMkBnbWFpbC5jb20iLCJleHAiOjE3ODMzMjQ3ODR9.AY-PMOH78_p-Jj9v3L1Hd_stU6NXcRWdmoBYHtVnjgo
def getUserDetail(): # token: str
    print("getUserDetail:", userps.user_id.get())
    userps.othr_userid.set(userps.user_id.get())
    user = getUserDataFromDB() # Execute Function to User Get Data
    if not user: # Invalid User
        raiseAPIError("User Not Found", 401)
    userps.first_name.set(user.first_name)
    userps.last_name.set(user.last_name)
    userps.email.set(user.email)
    user_dict = {
        "user_id": userps.user_id.get(),
        "role_id": userps.role_id.get(),
        "first_name": userps.first_name.get(),
        "last_name": userps.last_name.get(),
        "email": userps.email.get(),
    }
    user_dict.update(user.user_settings)
    # --------------------------
    # Get User Menu
    # --------------------------
    getUserMenuList(menups)
    # --------------------------
    # Get Workspace List
    # --------------------------
    getUserWSList(wsps)
    # --------------------------
    # Get Dashboard List
    # --------------------------
    getUserDashboards(dps)
    # --------------------------
    # Merge All Data & Send Response
    # --------------------------
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "User Data",
            "user_dict": user_dict,
            "menucentre_list": menups.menu_cntr_data.get(),
            "workspace_list" : wsps.ws_data.get(),
            "dashboard_list" : dps.dashboards_data.get()
        }
    )

def searchWSUser(request: Request):
    print("searchWSUser --> ")
    try:
        params = RequestData.params(request)
        userps.email.set(params.get("email", ""))
        if userps.email.get() in (None, ""):
            return raiseInvalidError("Invalid Email", 401)
        user = getUserDataFromDB()
        if user:
            user_data = {
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role_id": user.role_id
            }
            wsps.chk_ws_role.set(0)
            wsps.ws_usr_id.set(user.id)
            wsps.domain_flag.set(0)
            wsps.fetch_single.set(0)
            getUserWSData(wsps)
            userws_dtl = []
            for ws in wsps.ws_data.get():
                row = {
                    "workspace_id": getattr(ws, "workspace_id", 0),
                    "workspace_name": getattr(ws, "workspace_name", ""),
                    "ws_role_id": getattr(ws, "ws_role_id", 0),
                    "ws_role_lbl": getWSUserRole(int(ws.ws_role_id))
                }
                userws_dtl.append(row)
            user_data['userws_dtl'] = userws_dtl
            return JSONResponse(
                status_code = 200,
                content = {
                    "status": True,
                    "message": "User Data",
                    "user_data": user_data
                }
            )
        else:
            return raiseInvalidError("User Not Found", 401)
    except Exception as e:
        saveErrorLogtoDB ("User", userps.othr_userid.get(), "searchWSUser", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

async def updateUserProfile(request: Request):
    try:
        params = RequestData.params(request)
        setUserProperties(userps, params) # set params to user properties
        profile_pic = await RequestData.file(request, "profile_pic")
        if userps.othr_userid.get() in (None, "", 0):
            return raiseInvalidError("User Not Found", 401)
        # save profile pic in server
        userps.profile_pic.set(uploadFile(userps.ws_url.get(), "users", profile_pic))
        user = getUserDataFromDB()
        if user:
            user_settings = user.user_settings
            if userps.company_name.get() not in (None, ""):
                addUpdateJson(user_settings, "company_name", userps.company_name.get())
            if userps.user_timezone.get() not in (None, ""):
                addUpdateJson(user_settings, "time_zone", userps.user_timezone.get())
            if userps.profile_pic.get() not in (None, ""):
                addUpdateJson(user_settings, "profile_pic", userps.profile_pic.get())
            userps.user_settings.set(user_settings)
            userps.db_upd_vals.set({
                "first_name": userps.first_name.get(),
                "last_name": userps.last_name.get(),
                "phone": userps.phone.get(),
                "user_settings": userps.user_settings.get()
            })
            insertUpdateUserData()
        else:
            return raiseInvalidError("User Not Found", 401)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "User Profile Updated Successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB ("User", userps.othr_userid.get(), "updateUserProfile", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def changeUserPassword(request: Request):
    try:
        params = RequestData.params(request)
        userps.othr_userid.set(params.get("othr_userid", ""))
        userps.password.set(params.get("password", ""))
        if userps.othr_userid.get() in (None, "", 0):
            return raiseInvalidError("User Not Found", 401)
        user = getUserDataFromDB()
        if user:
            password = userps.password.get()
            password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            userps.db_upd_vals.set({"password": password.decode()})
            insertUpdateUserData()
        else:
            return raiseInvalidError("User Not Found", 401)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "User Password Updated Successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB ("User", userps.othr_userid.get(), "changeUserPassword", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def getUserList():
    print("getUserList:")
