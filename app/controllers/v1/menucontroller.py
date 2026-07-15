from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.properties.menuproperties import menups

# --------------------------
# Menu Centre
# --------------------------
def getMenuCentre(request: Request):
    print("getMenuCentre")

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