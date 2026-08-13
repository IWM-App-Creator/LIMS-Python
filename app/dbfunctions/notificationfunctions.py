from datetime import datetime
from app.utils.common import select, DB, userps, insert, update, func, not_, nowWithTimeZone, formatDate

def getNotificationList(notifyps):
    created_by = userps.user_id.get()
    pgno = int(notifyps.pgno.get() or 1)
    page_size = int(notifyps.page_size.get() or 10)
    view_id = int(notifyps.view_id.get() or 0)
    is_new = int(notifyps.is_new.get() or 0)
    is_read = int(notifyps.is_read.get() or 0)
    is_archive = int(notifyps.is_archive.get() or 0)
    is_delete = int(notifyps.is_delete.get() or 0)
    is_outbox = int(notifyps.is_outbox.get() or 0)
    if notifyps.created_by.get() not in (None, "", 0):
        created_by = notifyps.created_by.get()
    notificaitons = DB.getTableMeta("sys_notificaitons").alias("noti")
    dync_view = DB.getTableMeta("sys_new_dynamic_view").alias("dv")
    table_notes = DB.getTableMeta("sys_table_notes").alias("tn")
    from_user_data = DB.getTableMeta("users", "systemconfig").alias("from_user")
    to_user_data = DB.getTableMeta("users", "systemconfig").alias("to_user")
    stmt = (
        select(
            notificaitons,
            dync_view.c.url,
            dync_view.c.view_name,
            table_notes.c.parent_id,
            table_notes.c.item_id,
            func.concat(from_user_data.c.first_name, "**", from_user_data.c.last_name).label("from_user_name"),
            func.concat(to_user_data.c.first_name, "**", to_user_data.c.last_name).label("to_user_name"),
        )
        .outerjoin(
            dync_view,
            dync_view.c.view_id == notificaitons.c.view_id
        )
        .outerjoin(
            table_notes,
            table_notes.c.notes_id == notificaitons.c.notes_id
        )
        .outerjoin(
            from_user_data,
            from_user_data.c.id == notificaitons.c.created_by
        )
        .outerjoin(
            to_user_data,
            to_user_data.c.id == notificaitons.c.to_user_id
        )
        .where(notificaitons.c.created_date <= nowWithTimeZone())
        .order_by(notificaitons.c.notificaitons_id.desc())
    )
    if is_outbox in (None, "", 0):
        stmt = stmt.where(notificaitons.c.to_user_id == created_by)
    else:
        stmt = stmt.where(notificaitons.c.created_by == created_by)
        stmt = stmt.where(not_(notificaitons.c.noti_type.in_(['ShareWidget', 'CSVImport', 'CSVDownload'])))
    if is_new == 1:
        stmt = stmt.where(notificaitons.c.is_new == 1)
    if is_read == 1:
        stmt = stmt.where(notificaitons.c.is_read == 0)
    if is_read == 2:
        stmt = stmt.where(notificaitons.c.is_read == 1)
    if is_archive != 1:
        stmt = stmt.where(notificaitons.c.is_archive == 0)
    if is_delete in (None, "", 0):
        stmt = stmt.where(notificaitons.c.is_delete == 0)
    if view_id > 0:
        stmt = stmt.where(notificaitons.c.view_id == view_id)
    record_qry = select(func.count()).select_from(stmt.subquery())
    notifyps.record_cnt.set(DB.executeDBScalar(record_qry))
    offset = (pgno - 1) * page_size
    stmt = stmt.limit(page_size).offset(offset)
    return DB.executeDBSelect(stmt)

def getNotificationData(notifyps):
    notificaitons_id = int(notifyps.notificaitons_id.get() or 0)
    notificaitons = DB.getTableMeta("sys_notificaitons").alias("noti")
    stmt = select(notificaitons)
    stmt = stmt.where(notificaitons.c.notificaitons_id == notificaitons_id)
    return DB.executeDBSelectSingle(stmt)

def getUnreadNotiCount(notifyps):
    user_id = userps.user_id.get() # Get User ID
    tblnoti = DB.getTableMeta("sys_notificaitons").alias("noti")
    stmt = (
        select(func.count())
        .select_from(tblnoti)
        .where(
            tblnoti.c.is_read == 0,
            tblnoti.c.to_user_id == user_id,
            tblnoti.c.is_archive == 0,
            tblnoti.c.created_date <= nowWithTimeZone(),
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

def insertUpdateNotification(notifyps):    
    notificaitons = DB.getTableMeta("sys_notificaitons")
    notificaitons_id = int(notifyps.notificaitons_id.get() or 0)
    user_id = userps.user_id.get()
    created_date = nowWithTimeZone()
    if notifyps.created_date.get() not in (None, ""):
        created_date = notifyps.created_date.get()
    values = {}
    if notifyps.upd_vals.get() not in (None, "", {}):
        values = notifyps.upd_vals.get()
    else:
        if notifyps.noti_type.get() not in (None, ""):
            values["noti_type"] = notifyps.noti_type.get()
        if notifyps.item_id.get() not in (None, 0):
            values["item_id"] = notifyps.item_id.get()
        if notifyps.view_id.get() not in (None, 0):
            values["view_id"] = notifyps.view_id.get()
        if notifyps.table_id.get() not in (None, 0):
            values["table_id"] = notifyps.table_id.get()
        if notifyps.notes_id.get() not in (None, 0):
            values["notes_id"] = notifyps.notes_id.get()
        if notifyps.to_user_id.get() not in (None, 0):
            values["to_user_id"] = notifyps.to_user_id.get()
        if notifyps.title.get() not in (None, ""):
            values["title"] = notifyps.title.get()
        if notifyps.message.get() not in (None, ""):
            values["message"] = notifyps.message.get()
        if notifyps.msg_data.get() not in (None, ""):
            values["msg_data"] = notifyps.msg_data.get()
        if notifyps.is_read.get() not in (None, 0):
            values["is_read"] = notifyps.is_read.get()
        if notifyps.read_date.get() not in (None, ""):
            values["read_date"] = notifyps.read_date.get()
        if notifyps.is_new.get() not in (None, 0):
            values["is_new"] = notifyps.is_new.get()
        if notifyps.is_archive.get() not in (None, ""):
            values["is_archive"] = notifyps.is_archive.get()
    if notificaitons_id not in (None, "", 0):
        stmt = update(notificaitons).where(notificaitons.c.notificaitons_id == notificaitons_id).values(**values)
        DB.executeDBUpdate(stmt)
    else:
        values["created_by"] = user_id
        values["created_date"] = formatDate(created_date, "%Y-%m-%d %H:%M:%S")
        stmt = insert(notificaitons).values(**values)
        notificaitons_id = DB.executeDBInsert(stmt)
    return notificaitons_id