from datetime import datetime
from sqlalchemy import select, update, case, func
from app.utils.common import select, DB, userps

def getNotificationList(notifyps):
    view_id = viewps.view_id.get()
    user_id = userps.user_id.get()

    tblnoti = DB.tableMeta("sys_notificaitons").alias("noti")
    tblview = DB.tableMeta("sys_dynamic_view").alias("view")
    tblnotes = DB.tableMeta("sys_table_notes").alias("notes")
    tbluser = DB.getTableMeta("users", "systemconfig").alias("usr")
    viewdata = (
        select(
            func.concat(tblview.c.url, "~~", tblview.c.view_name)
        )
        .where(tblview.c.view_id == tblnoti.c.view_id)
        .scalar_subquery()
    )
    notesdata = (
        select(
            func.concat(tblnotes.c.parent_id, "~~", tblnotes.c.item_id)
        )
        .where(tblnotes.c.notes_id == tblnoti.c.notes_id)
        .scalar_subquery()
    )
    created_name = (
        select(
            func.concat(tbluser.c.first_name, "~~", tbluser.c.last_name)
        )
        .where(tbluser.c.id == tblnoti.c.created_by)
        .scalar_subquery()
    )
    to_usr_name = (
        select(
            func.concat(tbluser.c.first_name, "~~", tbluser.c.last_name)
        )
        .where(tbluser.c.id == tblnoti.c.to_user_id)
        .scalar_subquery()
    )
    stmt = select(
        tblnoti,
        case(
            (tblnoti.c.view_id > 0, viewdata),
            else_=""
        ).label("viewdata"),
        case(
            (tblnoti.c.notes_id > 0, notesdata),
            else_=""
        ).label("notesdata"),
        created_name.label("created_name"),
        to_usr_name.label("to_usr_name")
    )
    return DB.executeDBSelect(stmt)

def getUnreadNotiCount(notifyps):
    user_id = userps.user_id.get() # Get User ID
    tblnoti = DB.tableMeta("sys_notificaitons").alias("noti")
    stmt = (
        select(func.count())
        .select_from(tblnoti)
        .where(
            tblnoti.c.is_read == 0,
            tblnoti.c.to_user_id == user_id,
            tblnoti.c.is_archive == 0,
            tblnoti.c.created_date <= datetime.now(),
            tblnoti.c.is_delete == 0
        )
    )
    total_unread = DB.executeDBScalar(stmt)
    notifyps.total_unread.set(total_unread)

def markNotificationRead(notifyps):
    notificaitons_id = notifyps.notificaitons_id.get()
    item_id = notifyps.item_id.get()
    view_id = notifyps.view_id.get()
    table_id = notifyps.table_id.get()
    to_user_id = notifyps.to_user_id.get()
    tblnoti = DB.tableMeta("sys_notificaitons")
    stmt = update(tblnoti).values(
        is_read=1,
        is_new=0,
        read_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    if int(item_id) > 0 and int(table_id) > 0:
        stmt = stmt.where(
            tblnoti.c.item_id == item_id,
            tblnoti.c.table_id == table_id,
            tblnoti.c.to_user_id == to_user_id
        )
    elif int(view_id) > 0:
        stmt = stmt.where(
            tblnoti.c.view_id == view_id,
            tblnoti.c.to_user_id == to_user_id
        )
    elif str(view_id) == "-1":
        stmt = stmt.where(
            tblnoti.c.is_read == 0,
            tblnoti.c.to_user_id == to_user_id
        )
    else:
        stmt = stmt.where(
            tblnoti.c.notificaitons_id == notificaitons_id
        )
    DB.executeDBUpdate(stmt)

def markNotificationOld(notifyps):
    to_user_id = notifyps.to_user_id.get()
    tblnoti = DB.tableMeta("sys_notificaitons")
    stmt = (
        update(tblnoti)
        .where(
            tblnoti.c.is_new == 1,
            tblnoti.c.to_user_id == to_user_id
        )
        .values(
            is_new = 0
        )
    )
    DB.executeDBUpdate(stmt)

def markNotificationArchive(notifyps):
    item_id = notifyps.item_id.get()
    view_id = notifyps.view_id.get()
    table_id = notifyps.table_id.get()
    to_user_id = notifyps.to_user_id.get()
    tblnoti = DB.tableMeta("sys_notificaitons")
    update_data = {
        "is_archive": 1,
        "is_read": 1,
        "is_new": 0,
        "read_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    stmt = update(tblnoti).values(**update_data)
    if int(table_id) > 0 and int(item_id) > 0:
        stmt = stmt.where(
            tblnoti.c.table_id == table_id,
            tblnoti.c.item_id == item_id,
            tblnoti.c.to_user_id == to_user_id
        )
    elif int(view_id) > 0:
        stmt = stmt.where(
            tblnoti.c.view_id == view_id,
            tblnoti.c.to_user_id == to_user_id
        )
    elif str(view_id) == "-1":
        stmt = stmt.where(
            tblnoti.c.is_archive == 0,
            tblnoti.c.to_user_id == to_user_id
        )
    else:
        stmt = stmt.where(
            tblnoti.c.notificaitons_id == to_user_id
        )
    DB.executeDBUpdate(stmt)

def markNotificationDeleted(notifyps):
    flag = notifyps.flag.get()
    notificaitons_id = notifyps.notificaitons_id.get()
    to_user_id = notifyps.to_user_id.get()
    tblnoti = DB.tableMeta("sys_notificaitons")
    update_data = {
        "is_delete": 1
    }
    stmt = update(tblnoti)
    if int(flag) == 0:
        update_data.update({
            "is_read": 1,
            "is_new": 0,
            "read_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        stmt = stmt.where(
            tblnoti.c.notificaitons_id == notificaitons_id,
            tblnoti.c.to_user_id == to_user_id
        )
    else:
        stmt = stmt.where(
            tblnoti.c.is_delete == 0,
            tblnoti.c.to_user_id == to_user_id
        )
    stmt = stmt.values(**update_data)
    DB.executeDBUpdate(stmt)