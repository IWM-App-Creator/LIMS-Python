from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, globalps

# http://xytovet.localhost:8000/api/v1/notification/get
def getUserNotifications(request: Request):
    print("getUserNotifications --> ")

# http://xytovet.localhost:8000/api/v1/notification/markread
def markNotificationRead (request: Request):
    # try:
        # --------------------------
        # Get Input Parameters
        # --------------------------
        params = RequestData.params(request)
        user_id = params.get("user_id", "1")
        api_secret = params.get("api_secret", "")
        noti_id = params.get("noti_id", "")
        view_id = params.get("view_id", "0")
        item_id = params.get("item_id", "0")
        table_id = params.get("table_id", "0")
        
    #     tblnoti = DB.tableMeta("sys_notificaitons")
    #     data = {
    #         "is_read": 1,
    #         "is_new": 0,
    #         "read_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     }

    #     stmt = update(tblnoti).values(**data)

    #     if int(item_id) > 0 and int(table_id) > 0:
    #         stmt = stmt.where(
    #             tblnoti.c.item_id == item_id,
    #             tblnoti.c.table_id == table_id,
    #             tblnoti.c.to_user_id == user_id
    #         )

    #     elif int(view_id) > 0:
    #         stmt = stmt.where(
    #             tblnoti.c.view_id == view_id,
    #             tblnoti.c.to_user_id == user_id
    #         )

    #     elif str(view_id) == "-1":
    #         stmt = stmt.where(
    #             tblnoti.c.is_read == 0,
    #             tblnoti.c.to_user_id == user_id
    #         )

    #     else:
    #         stmt = stmt.where(
    #             tblnoti.c.notificaitons_id == noti_id
    #         )

    #     DB.executeDBUpdate(stmt)

    # except Exception as e:
    #     print("markNotificationRead:", e)

# http://xytovet.localhost:8000/api/v1/notification/markold
def markNotificationOld (request: Request):
    print("markNotificationOld --> ")

# http://xytovet.localhost:8000/api/v1/notification/delete
def markNotificationDeleted (request: Request):
    print("markNotificationDeleted --> ")

# http://xytovet.localhost:8000/api/v1/notification/archive
def markNotificationArchive (request: Request):
    print("getUserNotifications --> ")

# http://xytovet.localhost:8000/api/v1/notification/counts
def getNotiCountByUserID (request: Request):
    print("getNotiCountByUserID --> ")
