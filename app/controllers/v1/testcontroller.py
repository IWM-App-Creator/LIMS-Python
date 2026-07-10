from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, userps
from app.functions.associationhelper import getViewIdByAssociation, getCustomViewByAssociation, getMenuCenterByAssociation
from app.dbfunctions.associationfunctions import userAssociationView, getAssociationsForNotification
from app.properties.associationproperties import associationps

def getTestData(request: Request):
    print("getTestData --> ")
    associationps.user_id.set(userps.user_id.get())
    getViewIdByAssociation(associationps)
    getCustomViewByAssociation(associationps)
    getMenuCenterByAssociation(associationps)
    associationps.view_id.set(124)
    userAssociationView(associationps)
    asso_notify = getAssociationsForNotification(associationps)
    print("asso_notify --> ", asso_notify)

def saveTestData (request: Request):
    print("saveTestData --> ")
