import json
from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, nowWithTimeZone
from app.helper.notificationfunction import getNotifications, getNotificationCount, acceptNotificationData
from app.helper.generalfunctions import normalizeJson, getSelectedUsers
from app.dbfunctions.logfunctions import getDBErrorLogCount, saveErrorLogtoDB
from app.dbfunctions.notificationfunctions import getUnreadNotiCount, updateNotification, insertUpdateNotification
from app.properties.notificationproperties import notifyps
from app.properties.logproperties import logps

# http://xytovet.localhost:8000/api/v1/notification/get
def getUserNotifications(request: Request):
    print("getUserNotifications --> ")
    try:
        params = RequestData.params(request)
        notifyps.view_id.set(params.get("view_id", 0))
        notifyps.is_new.set(params.get("is_new", 0))
        notifyps.is_read.set(params.get("is_read", 0))
        notifyps.is_archive.set(params.get("is_archive", 0))
        notifyps.is_delete.set(params.get("is_delete", 0))
        notifyps.is_outbox.set(params.get("is_outbox", 0))
        notifyps.pgno.set(params.get("pgno", 1))
        notifyps.page_size.set(params.get("page_size", 10))
        notification_list = getNotifications(notifyps)
        getUnreadNotiCount(notifyps)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Notification List",
                "total_unread": notifyps.total_unread.get(),
                "rcrd_cnt": notifyps.record_cnt.get(),
                "notification_list": notification_list
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Notification", 0, "getUserNotifications", str(e))
        raiseAPIError(str(e), 500)

def getSystemStats(request: Request):
    print("getSystemStats --> ")
    try:
        params = RequestData.params(request)
        getUnreadNotiCount(notifyps)
        getDBErrorLogCount(logps)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "System Stat",
                "total_unread": notifyps.total_unread.get(),
                "error_count": logps.error_count.get(),
            }
        )
    except Exception as e:
        saveErrorLogtoDB("SystemStat", 0, "getSystemStats", str(e))
        raiseAPIError(str(e), 500)

def updateUserNotification(request: Request):
    try:
        params = RequestData.params(request)
        notificaitons_id = params.get("notificaitons_id")
        table_id = params.get("table_id")
        view_id = params.get("view_id")
        item_id = params.get("item_id")
        # At least one parameter must be provided
        if all(value in (None, "", 0, "0") for value in [notificaitons_id,table_id,view_id,item_id]):
            return raiseInvalidError("At least one of notificaitons_id, table_id, view_id or item_id is required", 200)
        notifyps.notificaitons_id.set(notificaitons_id or 0)
        notifyps.table_id.set(table_id or 0)
        notifyps.view_id.set(view_id or 0)
        notifyps.item_id.set(item_id or 0)
        notifyps.flag.set(params.get("flag", ""))
        updateNotification(notifyps)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Notification Updated Successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Notification",0,"updateUserNotification",str(e))
        raiseAPIError(str(e), 500)

def shareNotifications(request: Request):
    print("shareNotifications --> ")
    try:
        params = RequestData.params(request)
        view_id = params.get("view_id", 0)
        dashboard_id = params.get("dashboard_id", 0)
        widget_ref_id = params.get("widget_ref_id", "")
        save_id = params.get("save_id", 0)
        m_center_id = params.get("m_center_id", 0)
        noti_type = params.get("noti_type", None)
        message = params.get("message", None)
        save_name = params.get("save_name", None)
        share_users = normalizeJson(params.get("share_users", []), [])
        from_user = params.get("from_user", "")
        # Ensure it's a list
        if not isinstance(share_users, list):
            share_users = []
        title = ""
        msg_data = ""
        share_users = getSelectedUsers(share_users, view_id)
        if noti_type == "ShareWidget":
            title = from_user + " shared a widget with you."
            msg_data = json.dumps({"dashboard_id": dashboard_id, "widget_ref_id": widget_ref_id})
            sys_widgets_users_id = dashboard_id
        elif noti_type == "ShareMenu":
            title = save_name
            message = from_user + ' shared a menu "'  + save_name + '"'
            msg_data = json.dumps({"m_center_id": m_center_id})
            sys_widgets_users_id = m_center_id
        elif noti_type == "ShareFilter":
            title = save_name
            message = from_user + ' shared a filter view "' + save_name + '"'
            msg_data = json.dumps({"view_id": view_id, "save_id": save_id})
            sys_widgets_users_id = save_id
        share_users = list(dict.fromkeys(share_users))
        for usr in share_users:
            if usr:
                notifyps.upd_vals.set({
                    "noti_type": noti_type,
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
        saveErrorLogtoDB("Notification", 0, "shareNotifications", str(e))
        raiseAPIError(str(e), 500)

def acceptShareNotification(request: Request):
    print("acceptShareNotification --> ")
    try:
        params = RequestData.params(request)
        notifyps.flag.set(params.get("flag", ""))
        notifyps.notificaitons_id.set(params.get("notificaitons_id", 0) or 0)
        acceptNotificationData(notifyps)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Notification Updated Successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Notification", 0, "acceptShareNotification", str(e))
        raiseAPIError(str(e), 500)

def getNotiCountByViewID (request: Request):
    print("getNotiCountByViewID --> ")
    try:
        params = RequestData.params(request)
        notifyps.is_read.set(params.get("is_read", ""))
        notifyps.is_archive.set(params.get("is_archive", ""))
        views_notification = getNotificationCount(notifyps)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Notification Count List",
                "views_notification": views_notification
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Notification", 0, "getNotiCountByViewID", str(e))
        raiseAPIError(str(e), 500)
