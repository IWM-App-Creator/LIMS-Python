from app.utils.common import DB, select, JSONResponse, raiseAPIError, userps
from app.dbfunctions.userfunctions import getUserDataFromDB
from app.properties.dbproperties import dbps
from app.functions.menuhelper import getActiveMenuCenterID, setUserMenusOutput, setUserMenuCenterOutput
from app.functions.workspacehelper import setWorkspaceOutput
from app.functions.dashboardhelper import setDashboardOutput
from app.dbfunctions.menufunctions import getUserMenuList, getDynamicMenuCenter
from app.dbfunctions.workspacefunctions import getWorkspaceData
from app.dbfunctions.dashboardfunctions import getUserDashboards
from app.properties.menuproperties import menups
from app.properties.workspaceproperties import wsps
from app.properties.dashboardproperties import dps

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
    userps.user_settings.set(user.user_settings)
    user_dict = {
        "user_id": userps.user_id.get(),
        "role_id": userps.role_id.get(),
        "first_name": userps.first_name.get(),
        "last_name": userps.last_name.get(),
        "email": userps.email.get(),
        "user_settings": userps.user_settings.get(),
    }
    # --------------------------
    # Get User Menu
    # --------------------------
    menups.created_by.set(userps.user_id.get())
    menups.m_centre_id.set(None)
    menups.is_active.set(None)
    menups.is_public.set(None)
    menups.fetch_single.set(None)
    getDynamicMenuCenter(menups) # Get All Menu Centre By User
    getActiveMenuCenterID(menups) # find m_center_id from user_id
    getUserMenuList(menups) # Get User Active Menu
    setUserMenusOutput(menups) # Set Menu Output
    setUserMenuCenterOutput(menups) # Set Menu Centres
    # --------------------------
    # Get Workspace List
    # --------------------------
    wsps.domain_flag.set(0)
    wsps.fetch_single.set(0)
    getWorkspaceData(wsps)
    setWorkspaceOutput(wsps)
    # --------------------------
    # Get Dashboard List
    # --------------------------
    getUserDashboards(dps)
    setDashboardOutput(dps)
    # --------------------------
    # Merge All Data & Send Response
    # --------------------------
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "User Data",
            "user_dict": user_dict,
            "menu_centre": menups.menu_centre.get(),
            "active_menu_cid": menups.m_centre_id.get(),
            "user_menu": menups.menus_output.get(),
            "ws_list" : wsps.ws_data.get(),
            "dashboard_list" : dps.dashboards_data.get()
        }
    )

def getUserList():
    print("getUserList:")
