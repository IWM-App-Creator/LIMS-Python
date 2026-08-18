from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError

def downloadCSVData(request: Request):
    print("downloadCSVData --> ")
    try:
        params = RequestData.params(request)
    except Exception as e:
        raiseAPIError(str(e), 500)

def uploadCSVData(request: Request):
    print("uploadCSVData --> ")
    try:
        params = RequestData.params(request)
    except Exception as e:
        raiseAPIError(str(e), 500)