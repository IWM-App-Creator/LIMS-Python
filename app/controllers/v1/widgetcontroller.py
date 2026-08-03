from app.utils.common import Request, RequestData, raiseAPIError, JSONResponse, userps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.notificationfunctions import insertUpdateNotification
from app.dbfunctions.associationfunctions import getAssociationUsers
from app.helper.widgethelper import getWidgets, getUserWidgets
from app.properties.associationproperties import associationps
from app.properties.notificationproperties import notifyps
from app.properties.widgetproperties import widgetps

def getWidgetList(request: Request):
    print("getWidgetList --> ")
    try:
        params = RequestData.params(request)
        widgetps.dashboard_id.set(params.get("dashboard_id", 0))
        widgetps.view_id.set(params.get("view_id", 0))
        widgetps.sys_widget_cat_id.set(params.get("sys_widget_cat_id", None))
        widgetps.widget_type.set(params.get("widget_type", None))
        widgetps.search_text.set(params.get("search_text", None))
        widget_list = getWidgets(widgetps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Widget List",
                "widget_list": widget_list
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", widgetps.dashboard_id.get(), "getWidgetList", str(e))
        raiseAPIError(str(e), 500)

def getUserWidgetList(request: Request):
    print("getUserWidgetList --> ")
    try:
        params = RequestData.params(request)
        widgetps.dashboard_id.set(params.get("dashboard_id", 0))
        widgetps.sys_widget_id.set(params.get("sys_widget_id", 0))
        widgetps.preview.set(params.get("preview", 0))
        usrwdgt_list = getUserWidgets(widgetps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "User Widget List",
                "userwidget_list": usrwdgt_list
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", userps.user_id.get(), "getUserWidgetList", str(e))
        raiseAPIError(str(e), 500)

# api/v1/widget/share?view_id=182&sys_widgets_users_id=1&widget_type=ShareFilter&share_users=1,2,3&save_name=Test Filter
def shareUserWidget(request: Request):
    print("shareUserWidget --> ")
    try:
        params = RequestData.params(request)
        view_id = params.get("view_id", 0)
        sys_widgets_users_id = params.get("sys_widgets_users_id", 0)
        widget_type = params.get("widget_type", None)
        message = params.get("message", None)
        share_users = params.get("share_users", [])
        save_name = params.get("save_name", None)
        title = ""
        msg_data = ""
        if isinstance(share_users, str):
            share_users = share_users.split(",")
        if not isinstance(share_users, list):
            share_users = []
        if widget_type == "ShareWidget":
            title = userps.first_name.get() + " " + userps.last_name.get() + " shared a widget with you."
        elif widget_type == "ShareMenu":
            title = save_name
            message = userps.first_name.get() + " " + userps.last_name.get() + ' shared a menu "'  + save_name + '"'
            msg_data = {"m_center_id": sys_widgets_users_id}
        elif widget_type == "ShareFilter":
            title = save_name
            message = userps.first_name.get() + " " + userps.last_name.get() + ' shared a filter view "' + save_name + '"'
            msg_data = {"view_id": view_id, "save_id": sys_widgets_users_id}
            tmparr = []
            for user in share_users:
                if user.get("type") == 0:
                    tmparr.append(user.get("opt_val"))
                else:
                    associationps.is_notify.set(1)
                    associationps.col_p_val.set(user.get("opt_val"))
                    associationps.view_id.set(view_id)
                    associationps.fetch_single.set(0)
                    associationps.is_distinct.set(1)
                    assousers = getAssociationUsers(associationps)
                    for assousr in assousers:
                        tmparr.append(assousr.get("user_id"))
            share_users = tmparr
        share_users = list(dict.fromkeys(share_users))
        for usr in share_users:
            if usr:
                notifyps.upd_vals.set({
                    "noti_type": widget_type,
                    "item_id": sys_widgets_users_id,
                    "view_id": view_id,
                    "table_id": 0,
                    "notes_id": 0,
                    "to_user_id": usr,
                    "title": title,
                    "message": message,
                    "msg_data": msg_data
                })
                insertUpdateNotification(notifyps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "User Widget Shared Successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", userps.user_id.get(), "shareUserWidget", str(e))
        raiseAPIError(str(e), 500)