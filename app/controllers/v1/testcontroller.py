from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, globalps
from app.functions.notificationfunction import sendEmail
from app.properties.notificationproperties import notifyps

def getTestData (request: Request):
    print("getTestData --> ")
    notifyps.to_email = "rushirko05@gmail.com"
    notifyps.subject = "Test Email from LIMS-Python"
    notifyps.body = "Hello Good Morning, This is a test email from LIMS-Python. Please ignore this email."
    notifyps.html = ""
    notifyps.cc = ""
    notifyps.bcc = ""
    sendEmail()

def saveTestData (request: Request):
    print("saveTestData --> ")
