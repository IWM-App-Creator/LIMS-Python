from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.helper.filterhelper import getSaveFilters
from app.properties.filterproperties import filterps

def getFilters(request: Request):
    print("getFilters --> ")
    try:
        params = RequestData.params(request)
        filterps.view_id.set(params.get("view_id", 0))
        filter_list = getSaveFilters(filterps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Filter Data",
                "filter_list": filter_list
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Filter", filterps.view_id.get(), "getFilters", str(e))
        raiseAPIError(str(e), 500)