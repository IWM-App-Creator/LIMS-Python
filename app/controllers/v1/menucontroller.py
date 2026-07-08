from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, userps
from app.dbfunctions.associationfunctions import getAssociationUsers
from app.dbfunctions.menufunctions import getPublicOrUserMenuCenters, getDynamicMenuCenter, getUserMenuList
from app.properties.associationproperties import associationps
from app.properties.menuproperties import menups
from app.functions.menuhelper import setUserMenusOutput, setUserMenuCenterOutput

# --------------------------
# Menu Centre
# --------------------------
def getMenuCentre(request: Request):
    print("getMenuCentre --> ")
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
        raiseAPIError(str(e), 500)

def saveUserMenu(request: Request):
    print("saveUserMenu")
    

def updateUserMenu(request: Request):
    print("updateUserMenu")

def saveMenuSorting(request: Request):
    print("saveMenuSorting")

def removeUserMenu(request: Request):
    print("removeUserMenu")

def getMenuIcons(request: Request):
    print("getMenuIcons")
