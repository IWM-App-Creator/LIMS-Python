from app.utils.common import JSONResponse, Request, RequestData, raiseAPIError, raiseInvalidError
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.helper.systemviewhelper import getSystemView
from app.properties.systemviewproperties import systemviewps

def getSystemViewList(request: Request):
    try:
        params = RequestData.params(request)
        systemviewps.table_name.set(params.get("table_name", ""))
        systemviewps.schema_name.set(params.get("schema_name", None))
        if systemviewps.table_name.get() in (None, ""):
            return raiseInvalidError("Table Name Not Found", 401)
        systemview_list = getSystemView(systemviewps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "System View List",
                "systemview_list": systemview_list
            }
        )
    except Exception as e:
        saveErrorLogtoDB("System View", 0, "getSystemViewList", str(e))
        raiseAPIError(str(e), 500)