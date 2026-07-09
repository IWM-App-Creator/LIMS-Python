from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.dbfunctions.associationfunctions import getAssociationUsers
from app.dbfunctions.menufunctions import getPublicOrUserMenuCenters, getDynamicMenu, getDynamicMenuCenter, getUserMenuList, insertUpdateUserMenu
from app.functions.menuhelper import resetMenuProperties, setMenuInputParam, setUserMenusOutput, setUserMenuCenterOutput
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.customviewfunctions import addUpdateCustomView
from app.properties.menuproperties import menups
from app.properties.customviewproperties import customvwps

# --------------------------
# Menu Centre
# --------------------------
def getMenuCentre(request: Request):
    try:
        asso_menu_cntr_ids = [8, 51, 60, 61] # Get User Menu Centre IDs From Association Users
        menups.m_centre_ids.set(asso_menu_cntr_ids)
        mymenus = getPublicOrUserMenuCenters(menups) # Get User Menu Centre and Public Menu Centre
        menups.menu_array.set(mymenus)
        setUserMenuCenterOutput(menups)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Menu Centre Data",
                "menu_centres": menups.menus_output.get()
            }
        )
    except Exception as e:
        saveErrorLogtoDB ("Menu", 0, "getMenuCentre", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def saveMenuCentre(request: Request):
    print("saveMenuCentre")

def setMenuCentreActive(request: Request):
    print("setMenuCentreActive")

def resetMenuCentre(request: Request):
    print("resetMenuCentre")

def copyMenuCentre(request: Request):
    print("copyMenuCentre")

# --------------------------
# Menu
# --------------------------
def getUserMenu(request: Request):
    try:
        params = RequestData.params(request)
        menups.m_centre_id.set(params.get("m_centre_id", ""))
        if menups.m_centre_id.get() in (None, "", 0):
            return raiseInvalidError("Menu Center is not found", 404)
        menu_array = getUserMenuList(menups)
        menups.menu_array.set(menu_array)
        setUserMenusOutput(menups)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Menu Data",
                "menu_data": menups.menus_output.get()
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Menu", 0, "getUserMenu", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def saveUserMenu(request: Request):
    try:
        menu_id = ""
        status = True
        params = RequestData.params(request)
        menups.callfrom.set(params.get("callfrom", ""))
        menups.view_id.set(params.get("view_id", 0))
        is_valid = 1
        if menups.callfrom.get() == "ViewPage": # Call From User View Page
            menups.is_active.set(1)
            menups.created_by.set(userps.user_id.get())
            menups.fetch_single.set(1)
            menups.is_delete.set(0)
            menu_center = getDynamicMenuCenter(menups)
            if menu_center and menu_center.m_centre_id not in (None, "", 0):
                menups.m_centre_id.set(menu_center.m_centre_id)
            menups.is_delete.set(None)
            menups.m_type.set(1)
            user_menu = getDynamicMenu(menups)
            if user_menu:
                menu_id = user_menu.menu_id
                if user_menu.is_delete == 1:
                    menups.menu_id.set(user_menu.menu_id)
                    menups.m_type.set(0)
                    menups.is_delete.set(0)
                    menups.m_centre_id.set(None)
                    menups.created_by.set(None)
                    menups.view_id.set(None)
                    menups.is_new_tab.set(None)
                    menups.is_custom_centre.set(None)
                    menups.rank.set(None)
                    insertUpdateUserMenu(menups)
                    is_valid = 2
                else :
                    is_valid = 0
        if is_valid == 1:
            menups.fetch_single.set(1)
            menups.order_by.set("rank")
            menups.order_type.set("desc")
            menups.created_by.set(userps.user_id.get())
            menups.view_id.set(None)
            menups.m_centre_id.set(None)
            menups.m_type.set(0)
            user_menu = getDynamicMenu(menups)
            if user_menu:
                menups.rank.set(user_menu.rank + 1)
            setMenuInputParam(menups, params)
            menups.is_delete.set(0)
            menups.parent_menu_id.set(0)
            menu_id = insertUpdateUserMenu(menups)
            if menups.add_custom_view.get() == 1:
                resetMenuProperties(menups)
                menups.menu_id.set(menu_id)
                customvwps.view_name.set(menups.menu_name.get())
                customvwps.view_url.set(menups.menu_url.get())
                custom_view_id = addUpdateCustomView(customvwps)
                menups.view_id.set(custom_view_id)
                insertUpdateUserMenu(menups)
            status = True
        elif is_valid == 2:
            status = True
        else :
            status = False
        return JSONResponse (
            status_code = 200,
            content = {
                "status": status,
                "message": "Menu Saved Successfully",
                "menu_id": menu_id
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Menu", 0, "saveUserMenu", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def updateUserMenu(request: Request):
    print("updateUserMenu")

def saveMenuSorting(request: Request):
    print("saveMenuSorting")

def removeUserMenu(request: Request):
    print("removeUserMenu")

def getMenuIcons(request: Request):
    print("getMenuIcons")