from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.properties.menuproperties import menups
from app.dbfunctions.menufunctions import getMenuCentreData

# --------------------------
# Menu Centre
# --------------------------
def getMenuCentre(request: Request):
    print("getMenuCentre")
    try:
        asso_menu_cntr_ids = [8, 51, 60, 61] # Get User Menu Centre IDs From Association Users
        menups.m_centre_ids.set(asso_menu_cntr_ids)
        menu_centres = getMenuCentreData(menups)
        menu_centre = []
        for menu in menu_centres:
            menu_json = menu.menu_json
            if menu_json in (None, "", []):
                menu_json = []
            row = {
                "m_centre_id": menu.m_centre_id,
                "centre_name": menu.centre_name,
                "menu_json": menu_json,
                "short_desc": menu.short_desc,
                "preview_img": menu.preview_img,
                "is_public": menu.is_public,
                "is_active": menu.is_active,
                "created_by": menu.created_by
            }
            menu_centre.append(row)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Menu Centre Data",
                "menu_centres": menu_centre
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
    print("getUserMenu")

def saveUserMenu(request: Request):
    print("saveUserMenu")

def updateUserMenu(request: Request):
    print("updateUserMenu")

def saveMenuSorting(request: Request):
    print("saveMenuSorting --> ")

def removeUserMenu(request: Request):
    print("removeUserMenu")

def getMenuIcons(request: Request):
    print("getMenuIcons")