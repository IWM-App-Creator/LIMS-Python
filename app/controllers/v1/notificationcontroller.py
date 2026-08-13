from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError, nowWithTimeZone
from app.helper.notificationfunction import getNotifications, getNotificationCount
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.notificationfunctions import getUnreadNotiCount, updateNotification
from app.properties.notificationproperties import notifyps

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

def updateUserNotification(request: Request):
    try:
        params = RequestData.params(request)
        notifyps.notificaitons_id.set(params.get("notificaitons_id", 0))
        notifyps.table_id.set(params.get("table_id", 0))
        notifyps.view_id.set(params.get("view_id", 0))
        notifyps.item_id.set(params.get("item_id", 0))
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
        saveErrorLogtoDB("Notification", 0, "updateUserNotification", str(e))
        raiseAPIError(str(e), 500)

# http://xytovet.localhost:8000/api/v1/notification/counts
def getNotiCountByViewID (request: Request):
    print("getNotiCountByViewID --> ")
    try:
        params = RequestData.params(request)
        notifyps.is_read.set(params.get("is_read", 0))
        notifyps.is_archive.set(params.get("is_archive", 0))
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
