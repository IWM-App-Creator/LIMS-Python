import bcrypt
from app.utils.common import DB, select, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, nowWithTimeZone, globalps, userps
from app.dbfunctions.userfunctions import getUserDataFromDB, getUserListFromDB, insertUpdateUserData
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.workspacefunctions import getUserWSData, getWorkspaceData, getUserWorkspaceData, insertUpdateUsersWorkspace
from app.dbfunctions.associationfunctions import getAssociationsForNotification
from app.dbfunctions.dashboardfunctions import getDashboardData, insertUpdateDashboard
from app.properties.dbproperties import dbps
from app.helper.generalfunctions import uploadFile, addUpdateJson, getWSUserRole, generateRandomString
from app.helper.userhelper import setUserProperties
from app.helper.menuhelper import getUserMenuList
from app.helper.workspacehelper import getUserWSList
from app.helper.dashboardhelper import getUserDashboards
from app.helper.chatbothelper import ChatbotHelper as cbhlp
from app.helper.notificationfunction import sendEmail
from app.properties.menuproperties import menups
from app.properties.workspaceproperties import wsps
from app.properties.dashboardproperties import dps
from app.properties.chatbotproperties import cbps
from app.properties.associationproperties import associationps
from app.properties.notificationproperties import notifyps
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
            return raiseInvalidError("User Not Found", 200)
    except Exception as e:
        saveErrorLogtoDB ("User", userps.othr_userid.get(), "searchWSUser", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def inviteWorkspaceUser(request: Request):
    print("inviteWorkspaceUser --> ")
    try:
        params = RequestData.params(request)
        userps.first_name.set(params.get("first_name", ""))
        userps.last_name.set(params.get("last_name", ""))
        userps.email.set(params.get("email", ""))
        workspace_id = params.get("workspace_id", 0)
        role_id = params.get("role_id", 0)
        error_msg = "Something went wrong, Please try again!"
        password = generateRandomString(10, 1)
        workspace_name = ""
        workspace_url = ""
        # get workspace Data
        wsps.workspace_id.set(workspace_id)
        ws_data = getWorkspaceData(wsps)
        if ws_data:
            workspace_name = getattr(ws_data, "workspace_name", "")
            workspace_url = getattr(ws_data, "ws_url", "")
        # Set in System Users Table
        user_data = getUserDataFromDB()
        if user_data and user_data is not None:
            u_id = getattr(user_data, "id", 0)
            u_name = getattr(user_data, "first_name", "") + " " + getattr(user_data, "last_name", "")
            error_msg = 'User added to workspace "' + workspace_name + '" successfully.'
        else:
            u_name = userps.first_name.get() + " " + userps.last_name.get()
            newpassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            userps.db_upd_vals.set({
                "first_name": userps.first_name.get(),
                "last_name": userps.last_name.get(),
                "email": userps.email.get(),
                "password": newpassword.decode(),
                "role_id": role_id,
                "user_settings": {"active_ws": workspace_id, "pg_layout": "", "time_zone": "Australia/Perth", "user_sign": "", "public_key": "", "is_darkmode": 0, "profile_pic": "", "theme_color": "", "company_name": ""},
                "created_by": userps.user_id.get(),
                "created_at": nowWithTimeZone()
            })
            u_id = insertUpdateUserData()
            error_msg = 'User added to workspace "' + workspace_name + '" successfully.'
        # set in User Workspace Table
        wsps.ws_usr_id.set(u_id)
        user_ws = getUserWorkspaceData(wsps)
        if user_ws and user_ws is not None:
            wsps.user_wp_id.set(getattr(user_ws, "user_wp_id", 0))
            wsps.db_upd_vals.set({
                "is_delete": 0
            })
        else:  
            wsps.db_upd_vals.set({
                "user_id": u_id,
                "workspace_id": workspace_id,
                "ws_role_id": role_id,
                "is_invited": 1
            })
        insertUpdateUsersWorkspace(wsps)
        # send invitation email
        login_url = f"https://{workspace_url}.{globalps.APP_DOMAIN}/login"
        # Email subject
        subject = f"Welcome to {workspace_name}"
        # Email HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{subject}</title>
        </head>
        <body style="font-family: Arial, sans-serif; color: #333;">

            <h2>Welcome to {workspace_name}</h2>

            <p>Hi {u_name},</p>

            <p>
                Your account has been created successfully.
                You can use the following credentials to log in:
            </p>

            <table cellpadding="8" cellspacing="0" border="0">
                <tr>
                    <td><strong>Name:</strong></td>
                    <td>{u_name}</td>
                </tr>
                <tr>
                    <td><strong>Email:</strong></td>
                    <td>{userps.email.get()}</td>
                </tr>
                <tr>
                    <td><strong>Password:</strong></td>
                    <td>{password}</td>
                </tr>
            </table>

            <p>
                <a href="{login_url}"
                   style="
                       display: inline-block;
                       padding: 10px 20px;
                       background-color: #007bff;
                       color: white;
                       text-decoration: none;
                       border-radius: 5px;
                   ">
                    Login to Workspace
                </a>
            </p>

            <p>
                Or copy and paste the following URL into your browser:
            </p>

            <p>{login_url}</p>

            <br>

            <p>Regards,<br>
            MiiData</p>

        </body>
        </html>
        """
        notifyps.subject.set(subject)
        notifyps.to_email.set(userps.email.get())
        notifyps.cc.set("")
        notifyps.bcc.set("miidata@genotypingaustralia.com.au")
        notifyps.html.set(html)
        notifyps.body.set("")
        notifyps.attachments.set([])
        # Send email
        sendEmail(notifyps)
        # create Default Dashboard
        dps.created_by.set(u_id)
        dash_data = getDashboardData(dps)
        if not dash_data:
            dps.db_upd_vals.set({
                "dashboard_name": "Default",
                "widget_list": [{"x": "0", "y": "0", "c_width": "3", "bg_color": "#ffffff", "c_height": "1.5", "htm_flow": "0", "widget_label": "Add Menu", "sys_widget_id": "1", "widget_ref_id": generateRandomString(10, 1), "widget_setting": {}}, {"x": "0", "y": "0", "c_width": "3", "bg_color": "#ffffff", "c_height": "1.5", "htm_flow": "0", "widget_label": "Add View", "sys_widget_id": "2", "widget_ref_id": generateRandomString(10, 1), "widget_setting": {}}, {"x": "0", "y": "0", "c_width": "3", "bg_color": "#ffffff", "c_height": "1.5", "htm_flow": "0", "widget_label": "Add User", "sys_widget_id": "3", "widget_ref_id": generateRandomString(10, 1), "widget_setting": {}}],
                "is_active": 1
            })
            insertUpdateDashboard(dps)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": error_msg,
                "u_id": u_id,
                "first_name": userps.first_name.get(),
                "last_name": userps.last_name.get(),
            }
        )
    except Exception as e:
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
            userps.othr_userid.set(getattr(user, "id", 0))
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
            userps.othr_userid.set(getattr(user, "id", 0))
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