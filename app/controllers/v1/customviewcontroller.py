from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.customviewfunctions import addUpdateCustomView
from app.properties.customviewproperties import customvwps

def saveCustomView(request: Request):
    print("saveCustomView --> ")
    try:
        params = RequestData.params(request)
        customvwps.custom_view_id.set(params.get("custom_view_id", 0))
        customvwps.view_name.set(params.get("view_name", ""))
        customvwps.view_url.set(params.get("view_url", ""))
        addUpdateCustomView(customvwps)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Custom View Saved Successfully",
                "custom_view_id": customvwps.custom_view_id.get()
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Custom View", 0, "saveCustomView", str(e))
        raiseAPIError(str(e), 500)