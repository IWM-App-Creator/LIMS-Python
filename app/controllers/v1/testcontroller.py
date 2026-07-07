from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, userps
from app.functions.notificationfunction import sendEmail
from app.dbfunctions.associationfunctions import getAssociationUsers
from app.dbfunctions.menufunctions import getDynamicMenuCenter, getUserMenuList
from app.properties.notificationproperties import notifyps
from app.properties.associationproperties import associationps
from app.properties.menuproperties import menups

def getTestData(request: Request):
    print("getTestData --> ")
    menups.is_active.set(1)
    menucenter = getDynamicMenuCenter()
    print("menucenter --> ")
    for row in menucenter:
        print(dict(row._mapping))
    return
    if menucenter and menucenter[0]["m_centre_id"] > 0:
        menups.m_centre_id.set(menucenter[0]["m_centre_id"])
    else :
        associationps.user_id.set(userps.user_id.get())
        association_mnu = getAssociationUsers()
        if association_mnu and association_mnu[0]["defmenucntr"] > 0:
            menups.m_centre_id.set(association_mnu[0]["defmenucntr"])
            menups.usr_flag.set(1)
    sidemenus = getUserMenuList()
    print("sidemenus --> ", sidemenus)

def saveTestData (request: Request):
    print("saveTestData --> ")
