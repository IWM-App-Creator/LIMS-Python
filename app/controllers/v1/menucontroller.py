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
        getPublicOrUserMenuCenters(menups) # Get User Menu Centre and Public Menu Centre
        setUserMenuCenterOutput(menups)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Menu Centre Data",
                "menu_centres": menups.menu_centre.get()
            }
        )
    except Exception as e:
        # saveErrorLogtoDB ("Menu", 0, "getMenuCentre", str(e)) # Log Error To DB
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
        getUserMenuList(menups)
        menups.menu_array.set(menups.menu_cntr_data.get())
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
        # saveErrorLogtoDB("Menu", 0, "getUserMenu", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def saveUserMenu(request: Request):
    try:
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
            getDynamicMenuCenter(menups)
            menu_centre = menups.menu_centre.get()
            if menu_centre and menu_centre.m_centre_id not in (None, "", 0):
                menups.m_centre_id.set(menu_centre.m_centre_id)
            menups.is_delete.set(None)
            menups.m_type.set(1)
            getDynamicMenu(menups)
            user_menu = menups.menu_cntr_data.get()
            if user_menu:
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
            getDynamicMenu(menups)
            user_menu = menups.menu_cntr_data.get()
            if user_menu:
                menups.rank.set(user_menu.rank + 1)
            setMenuInputParam(menups, params)
            menups.is_delete.set(0)
            menups.parent_menu_id.set(0)
            insertUpdateUserMenu(menups)
            if menups.add_custom_view.get() == 1:
                resetMenuProperties(menups)
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
                "menu_id": menups.menu_id.get()
            }
        )
    except Exception as e:
        # saveErrorLogtoDB("Menu", 0, "saveUserMenu", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def updateUserMenu(request: Request):
    try:
        params = RequestData.params(request)
        setMenuInputParam(menups, params)
        if menups.menu_id.get() in (None, "", 0):
            return raiseInvalidError("Menu Id is not found", 404)
        insertUpdateUserMenu(menups)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Menu Updated Successfully"
            }
        )
    except Exception as e:
        # saveErrorLogtoDB("Menu", menups.menu_id.get(), "updateUserMenu", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def saveMenuSorting(request: Request):
    print("saveMenuSorting --> ")
    try:
        tempmenuarr = []
        status = False
        params = RequestData.params(request)
        menuids = params.get("menuids", None)
        if menuids in (None, ""):
            return raiseInvalidError("Menu Ids is not found", 404)
        if isinstance(menuids, str):
            menuids = menuids.strip(",")
            menuids = menuids.split(",")
        rank = 1
        for menu in menuids:
            resetMenuProperties(menups)
            childarr = menu.split("-")
            menups.menu_id.set(childarr[0] if childarr[0] else 0)
            menups.parent_menu_id.set(0)
            menups.rank.set(rank)
            insertUpdateUserMenu(menups)
            rank = rank + 1
            if len(childarr) > 1:
                parentmenu1 = menups.menu_id.get()
                for chilf in childarr[1:]:
                    childarr2 = chilf.split("|")
                    menups.menu_id.set(childarr2[0] if childarr2[0] else 0)
                    menups.parent_menu_id.set(parentmenu1)
                    menups.rank.set(rank)
                    insertUpdateUserMenu(menups)
                    rank = rank + 1
                    parentmenu = menups.menu_id.get()
                    for chilf2 in childarr2[1:]:
                        menups.menu_id.set(chilf2 if chilf2 else 0)
                        menups.parent_menu_id.set(parentmenu)
                        menups.rank.set(rank)
                        insertUpdateUserMenu(menups)
                        rank = rank + 1
            tempmenuarr.append(menups.parent_menu_id.get())
        status = True
        return JSONResponse (
            status_code = 200,
            content = {
                "status": status,
                "message": "Menu Sorted Successfully",
                "parent_menu_id": tempmenuarr
            }
        )
    except Exception as e:
        # saveErrorLogtoDB("Menu", 0, "saveMenuSorting", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)


def removeUserMenu(request: Request):
    print("removeUserMenu")

def getMenuIcons(request: Request):
    print("getMenuIcons")