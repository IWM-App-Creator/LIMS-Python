from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, globalps
from app.functions.notificationfunction import sendEmail
from app.dbfunctions.associationfunctions import getAssociationUsers
from app.dbfunctions.menufunctions import getUserMenuList
from app.properties.notificationproperties import notifyps
from app.properties.associationproperties import associationps

def getTestData(request: Request):
    print("getTestData --> ")
    # params = RequestData.params(request)
    # notifyps.to_email.set(params.get("to_email", ""))
    # notifyps.subject.set(params.get("subject", ""))
    # notifyps.body.set(params.get("body", ""))
    # notifyps.html.set(params.get("html", ""))
    # notifyps.cc.set(params.get("cc", ""))
    # notifyps.bcc.set(params.get("bcc", ""))
    # notifyps.attachments.set(params.get("attachments", []))
    # sendEmail()
    getUserMenuList(3837)

def saveTestData (request: Request):
    print("saveTestData --> ")
