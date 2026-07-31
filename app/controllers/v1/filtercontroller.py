from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError, userps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.notificationfunctions import getNotificationData, insertUpdateNotification
from app.dbfunctions.filterfunctions import insertUpdateFilter, getFilterData
from app.dbfunctions.widgetfunctions import getWidgetData, insertUpdateWidget
from app.helper.filterhelper import getSaveFilters
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
        filterps.view_qry_json.set(params.get("view_qry_json", []))
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

# api/v1/filter/copy
def copySaveFilterView(request: Request):
    print("copySaveFilterView --> ")
    try:
        params = RequestData.params(request)
        notifyps.notificaitons_id.set(params.get("notificaitons_id", 0))
        flag = params.get("flag", "")
        message = "Invalid Request"
        if flag == "remove":
            notifyps.upd_vals.set({"is_delete": 1})
            message = "Filter Deleted Successfully"
        elif flag == "savefilter" or flag == "addtodashboard":
            message = "Filter Saved Successfully"
            notification = getNotificationData(notifyps)
            if notification is not None and getattr(notification, "msg_data", "") not in (None, ""):
                msg_data = getattr(notification, "msg_data", {})
                if not isinstance(getattr(notification, "msg_data", {}), dict):
                    msg_data = {}
                view_id = int(msg_data.get("view_id", 0))
                save_id = int(msg_data.get("save_id", 0))
                filterps.save_id.set(save_id)
                filter = getFilterData(filterps)
                if filter is not None:
                    filterps.save_id.set(None)
                    filterps.save_name.set(getattr(filter, "save_name", ""))
                    filterps.view_id.set(view_id)
                    filterps.view_qry_json.set(getattr(filter, "view_qry_json", []))
                    new_save_id = insertUpdateFilter(filterps)
                    if flag == "addtodashboard":
                        message = "Filter added to Dashboard Successfully"
                        widget_json = {"view_id": view_id, "save_id": new_save_id, "pgno": ""}
                        widgetps.widget_json.set(widget_json)
                        widgetps.widget_type.set("VIEWWIDGET")
                        widgetps.view_id.set(view_id)
                        widgetps.created_by.set(userps.user_id.get())
                        widgetps.fetch_single.set(1)
                        widget = getWidgetData(widgetps)
                        if widget is None:
                            widgetps.sys_widget_cat_id.set(2)
                            widgetps.widget_title.set(getattr(filter, "save_name", ""))
                            widgetps.is_multiple.set(0)
                            widgetps.is_global.set(0)
                            widgetps.is_system.set(0)
                            widgetps.is_delete.set(0)
                            insertUpdateWidget(widgetps)
            notifyps.upd_vals.set({"msg_data": ""})
        insertUpdateNotification(notifyps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": message
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Filter", filterps.save_id.get(), "copySaveFilterView", str(e))
        raiseAPIError(str(e), 500)

# api/v1/filter/setdefault
def makeDefaultFilter(request: Request):
    print("makeDefaultFilter --> ")
    try:
        params = RequestData.params(request)
        filterps.save_id.set(params.get("save_id", 0))
        filterps.is_default.set(params.get("is_default", 0))
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