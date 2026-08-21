import json
from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError, userps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.notificationfunctions import getNotificationData, insertUpdateNotification
from app.dbfunctions.filterfunctions import insertUpdateFilter, getFilterData
from app.dbfunctions.widgetfunctions import getWidgetData, insertUpdateWidget
from app.helper.filterhelper import getSaveFilters
from app.helper.generalfunctions import normalizeJson
from app.properties.filterproperties import filterps
from app.properties.widgetproperties import widgetps
from app.properties.notificationproperties import notifyps

# api/v1/filter/get
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

# api/v1/filter/save
def saveViewFilter(request: Request):
    print("saveViewFilter --> ")
    try:
        params = RequestData.params(request)
        filterps.save_id.set(params.get("save_id", 0))
        filterps.save_name.set(params.get("save_name", ""))
        filterps.view_id.set(params.get("view_id", 0))
        filterps.view_qry.set(params.get("view_qry", ""))
        view_qry_json = normalizeJson(params.get("view_qry_json", []), [])
        if not isinstance(view_qry_json, list):
            view_qry_json = []
        filterps.view_qry_json.set(view_qry_json)
        filterps.is_default.set(params.get("is_default", 0))
        insertUpdateFilter(filterps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Filter Saved Successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Filter", filterps.view_id.get(), "saveViewFilter", str(e))
        raiseAPIError(str(e), 500)

# api/v1/filter/setdefault
def makeDefaultFilter(request: Request):
    print("makeDefaultFilter --> ")
    try:
        params = RequestData.params(request)
        filterps.view_id.set(params.get("view_id", 0))
        filterps.save_id.set(params.get("save_id", 0))
        filterps.is_default.set(1)
        filterps.upd_vals.set({"is_default": 1})
        insertUpdateFilter(filterps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Default Filter Set Successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Filter", filterps.save_id.get(), "makeDefaultFilter", str(e))
        raiseAPIError(str(e), 500)

# api/v1/filter/remove
def removeSaveFilterView(request: Request):
    print("removeSaveFilterView --> ")
    try:
        params = RequestData.params(request)
        filterps.save_id.set(params.get("save_id", 0))
        filterps.is_delete.set(1)
        filterps.upd_vals.set({"is_delete": 1})
        insertUpdateFilter(filterps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Filter Deleted Successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Filter", filterps.save_id.get(), "removeSaveFilterView", str(e))
        raiseAPIError(str(e), 500)