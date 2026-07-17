import json
from app.utils.common import DB, select, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.dbfunctions.userfunctions import getUserDataFromDB, insertUpdateUserData
from app.properties.dbproperties import dbps
from app.helper.generalfunctions import uploadFile, addUpdateJson
from app.helper.menuhelper import getUserMenuList
from app.helper.workspacehelper import getUserWSList
from app.helper.dashboardhelper import getUserDashboards
from app.properties.menuproperties import menups
from app.properties.workspaceproperties import wsps
from app.properties.dashboardproperties import dps
from fastapi import UploadFile, File

# http://xytovet.localhost:8000/api/v1/user/getdetail?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzc3OSIsInJvbGVfaWQiOiIxIiwiZW1haWwiOiJjaGludGFuaXQyMkBnbWFpbC5jb20iLCJleHAiOjE3ODMzMjQ3ODR9.AY-PMOH78_p-Jj9v3L1Hd_stU6NXcRWdmoBYHtVnjgo
def getUserDetail(): # token: str
    print("getUserDetail:", userps.user_id.get())
    # --------------------------
    # Get User Data
    # --------------------------
    # tbluser = DB.getTableMeta("users", "systemconfig").alias("usr")
    # stmt = (
    #     select(tbluser).where(tbluser.c.id == userps.user_id.get())
    # )
    # user = DB.executeDBSelectSingle(stmt)
    # if not user: # Invalid User
    #     raiseAPIError("Invalid User ID", 401)

    user = getUserDataFromDB() # Execute Function to User Get Data
    if not user: # Invalid User
        raiseAPIError("Invalid Email", 401)
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
            "menu_centre": menups.menu_cntr_data.get(),
            "ws_list" : wsps.ws_data.get(),
            "dashboard_list" : dps.dashboards_data.get()
        }
    )

async def updateUserProfile(user_id: int, first_name: str, last_name: str, phone: str, company_name: str, timezone: str, profile_pic: UploadFile = File(...)):
    # params = RequestData.params(request)
    # userps.user_id.set(params.get("user_id", ""))
    # userps.othr_userid.set(params.get("othr_userid", ""))
    # userps.first_name.set(params.get("first_name", ""))
    # userps.last_name.set(params.get("last_name", ""))
    # userps.phone.set(params.get("phone", ""))
    # userps.company_name.set(params.get("company_name", ""))
    # userps.user_timezone.set(params.get("timezone", ""))
    # profile_pic = await RequestData.file(request, "profile_pic")
    userps.user_id.set(user_id)
    userps.first_name.set(first_name)
    userps.last_name.set(last_name)
    userps.phone.set(phone)
    userps.company_name.set(company_name)
    userps.user_timezone.set(timezone)
    # profile_pic = await RequestData.file(request, "profile_pic")
    userps.profile_pic.set(profile_pic)
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
        userps.db_upd_vals.set(
            {
                "first_name": userps.first_name.get(),
                "last_name": userps.last_name.get(),
                "phone": userps.phone.get(),
                "user_settings": userps.user_settings.get()
            }
        )
        insertUpdateUserData()
    else:
        return raiseInvalidError("User Not Found", 401)

def getUserList():
    print("getUserList:")
