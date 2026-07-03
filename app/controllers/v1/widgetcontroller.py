from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, globalps

def getTestData (request: Request):
    print("getTestData --> ")
