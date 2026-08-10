from app.utils.common import DB, select, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.dbfunctions.userfunctions import getUserDataFromDB, getUserListFromDB, insertUpdateUserData
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.workspacefunctions import getUserWSData
from app.dbfunctions.associationfunctions import getAssociationsForNotification
from app.properties.dbproperties import dbps
from app.helper.generalfunctions import uploadFile, addUpdateJson, getWSUserRole
from app.helper.userhelper import setUserProperties
from app.helper.menuhelper import getUserMenuList
from app.helper.workspacehelper import getUserWSList
from app.helper.dashboardhelper import getUserDashboards
from app.helper.chatbothelper import ChatbotHelper as cbhlp
from app.properties.menuproperties import menups
from app.properties.workspaceproperties import wsps
from app.properties.dashboardproperties import dps
from app.properties.chatbotproperties import cbps
from app.properties.associationproperties import associationps
from app.helper.generalfunctions import formatUserDisplayName

# http://xytovet.localhost:8000/api/v1/user/getdetail?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzc3OSIsInJvbGVfaWQiOiIxIiwiZW1haWwiOiJjaGludGFuaXQyMkBnbWFpbC5jb20iLCJleHAiOjE3ODMzMjQ3ODR9.AY-PMOH78_p-Jj9v3L1Hd_stU6NXcRWdmoBYHtVnjgo

def getUserDetail(request: Request): # token: str
    try:
        userps.othr_userid.set(userps.user_id.get())
        user = getUserDataFromDB() # Execute Function to User Get Data
        if not user: # Invalid User
            raiseAPIError("User Not Found", 404)
        userps.first_name.set(user.first_name)
        userps.last_name.set(user.last_name)
        userps.email.set(user.email)
        userps.user_settings.set(user.user_settings)
        # --------------------------
        # Get User Menu
        # --------------------------
        menups.created_by.set(userps.user_id.get())
        getUserMenuList(menups)
        # --------------------------
        # Get Workspace List
        # --------------------------
        getUserWSList(wsps)
        # --------------------------
        # Get Dashboard List
        # --------------------------
        dps.created_by.set(userps.user_id.get())
        getUserDashboards(dps)
        # --------------------------
        # Get Dashboard List
        # --------------------------
        cbhlp.getUserCBModules(cbps)
        # --------------------------
        # Merge All Data & Send Response
        # --------------------------
        user_dict = {
            "user_id": userps.user_id.get(),
            "role_id": userps.role_id.get(),
            "first_name": userps.first_name.get(),
            "last_name": userps.last_name.get(),
            "email": userps.email.get(),
        }
        user_dict.update(user.user_settings)
        user_dict.update({"active_ws_name": wsps.workspace_name.get() or "", "active_menu": int(menups.m_centre_id.get() or 0),"active_menu_name": menups.centre_name.get() or "", "active_dashboard": int(dps.dashboard_id.get() or 0), "active_dashboard_name": dps.dashboard_name.get() or "", "ws_role_id": int(wsps.ws_role_id.get() or 0)})
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "User Data",
                "user_dict": user_dict,
                "menucentre_list": menups.menu_cntr_data.get(),
                "workspace_list" : wsps.ws_data.get(),
                "dashboard_list" : dps.dashboards_data.get(),
                "cb_module_list": cbps.cb_md_list.get(),
            }
        )
    except Exception as e:
        # saveErrorLogtoDB ("User", "", "getUserList", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def getUserList(request: Request):
    try:
        params = RequestData.params(request)
        view_id = int(params.get("view_id", 0))
        ws_flag = params.get("ws_flag", "")
        ws_ws_id = int(params.get("ws_ws_id", 0))
        # Set Workspace ID To Get User List
        if ws_flag == "wsflag" and ws_ws_id > 0 : 
            userps.ws_ws_id.set(ws_ws_id)  # Set Pass Workspace ID
        else :
            userps.ws_ws_id.set(userps.workspace_id.get()) # Set User Workspace ID
        users = getUserListFromDB(userps)
        item_list = []
        if not users: # Invalid View
            return raiseAPIError("User Not Found", 200)
        for user in users:
            first_name = getattr(user, "first_name", "")
            last_name = getattr(user, "last_name", "")
            email = getattr(user, "email", "")
            user_name = "";
            if first_name:
                user_name = formatUserDisplayName(first_name=first_name, last_name=last_name)
                if ws_flag == "wsflag":
                    user_name += f"<span style='font-size: 12px; padding-left:2px;'>({email})</span>"
            else :
                user_name = email
            item = {
                "opt_val": user.id,
                "label": user_name,
                "type": 0,
            }
            item_list.append(item)
        # Include Users Groups Based On Permission
        if view_id not in ("", None, 0):
            associationps.view_id.set(view_id)
            associationps.user_id.set(userps.user_id.get())
            grouparr = getAssociationsForNotification(associationps)
            if grouparr not in (None, "", []):
                for group in grouparr:
                    row = {
                        "opt_val": group.get("value", 0),
                        "label": group.get("label", ""),
                        "type": 1
                    }
                    item_list.append(row)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Users List",
                "user_data": item_list
            }
        )
    except Exception as e:
        # saveErrorLogtoDB ("User", "", "getUserList", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def saveLinkedUser(request: Request):
    print("saveLinkedUser --> ")
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