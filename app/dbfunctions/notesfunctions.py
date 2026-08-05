import datetime
from app.utils.common import DB, select, insert, update, or_, func, and_, formatDate, userps, nowWithTimeZone

def getNotes(notesps):
    tbl_notes = DB.getTableMeta("sys_table_notes").alias("notes")
    users = DB.getTableMeta("users", "systemconfig").alias("usr")
    stmt = (
        select(
            tbl_notes,
            users.c.first_name,
            users.c.last_name
        )
        .outerjoin(
            users,
            users.c.id == tbl_notes.c.created_by
        )
    )
    if notesps.view_id.get() not in (None, "", 0):
        stmt = stmt.where(tbl_notes.c.view_id == notesps.view_id.get())
    if notesps.item_id.get() not in (None, "", 0):
        stmt = stmt.where(tbl_notes.c.item_id == notesps.item_id.get())
    if notesps.showdel.get() in (None, "", 0, "0"):
        stmt = stmt.where(tbl_notes.c.is_delete == 0)
    stmt = stmt.where(
        or_(
            tbl_notes.c.created_date <= nowWithTimeZone(),
            tbl_notes.c.created_by == userps.user_id.get()
        )
    )
    stmt = stmt.order_by(tbl_notes.c.notes_id.asc())
    return DB.executeDBSelect(stmt)

def getFromUsersData(notesps):
    note_ids = notesps.note_ids.get()
    view_id = notesps.view_id.get()
    if not note_ids:
        return []
    tbl_notification = DB.getTableMeta("sys_notificaitons").alias("nt")
    users = DB.getTableMeta("users", "systemconfig").alias("from_usr")
    stmt_from = (
        select(
            tbl_notification.c.notes_id,
            users.c.id,
            users.c.first_name,
            users.c.last_name
        )
        .distinct()
        .outerjoin(
            users,
            users.c.id == tbl_notification.c.created_by
        )
        .where(
            tbl_notification.c.view_id == view_id,
            tbl_notification.c.notes_id.in_(note_ids)
        )
        .order_by(tbl_notification.c.notes_id.desc())
    )
    if notesps.showdel.get() in (None, "", 0, "0"):
        stmt_from = stmt_from.where(tbl_notification.c.is_delete == 0)
    return DB.executeDBSelect(stmt_from)

def getToUsersData(notesps):
    note_ids = notesps.note_ids.get()
    view_id = notesps.view_id.get()
    if not note_ids:
        return []
    tbl_notification = DB.getTableMeta("sys_notificaitons").alias("nt")
    users = DB.getTableMeta("users", "systemconfig").alias("to_usr")
    stmt_from = (
        select(
            tbl_notification.c.notes_id,
            users.c.id,
            users.c.first_name,
            users.c.last_name,
            tbl_notification.c.is_read
        )
        .distinct()
        .outerjoin(
            users,
            users.c.id == tbl_notification.c.to_user_id
        )
        .where(
            tbl_notification.c.view_id == view_id,
            tbl_notification.c.notes_id.in_(note_ids)
        )
        .order_by(tbl_notification.c.notes_id.desc())
    )
    if notesps.showdel.get() in (None, "", 0, "0"):
        stmt_from = stmt_from.where(tbl_notification.c.is_delete == 0)
    return DB.executeDBSelect(stmt_from)

def getSmileyNotes(notesps):
    note_ids = notesps.note_ids.get()
    if note_ids in (None, ""):
        return []
    if isinstance(note_ids, str):
        note_ids = note_ids.split(",")
    notes_smiley = DB.getTableMeta("sys_table_notes_smiley").alias("notes_smiley")
    users = DB.getTableMeta("users", "systemconfig").alias("usr")
    stmt = (
        select(
            notes_smiley,
            users.c.first_name,
            users.c.last_name
        )
        .outerjoin(
            users,
            users.c.id == notes_smiley.c.created_by
        )
        .where(notes_smiley.c.notes_id.in_(note_ids))
        .where(notes_smiley.c.is_delete == 0)
    )
    return DB.executeDBSelect(stmt)

def insertUpdateNotes(notesps):
    notes_id = int(notesps.notes_id.get() or 0)
    view_id = int(notesps.view_id.get() or 0)
    table_id = int(notesps.table_id.get() or 0)
    col_id = int(notesps.col_id.get() or 0)
    item_id = int(notesps.item_id.get() or 0)
    table_notes = DB.getTableMeta("sys_table_notes")
    created_date = nowWithTimeZone()
    if notesps.reminder_date.get() not in (None, ""):
        created_date = notesps.reminder_date.get()
    values = {}
    if notesps.upd_vals.get() not in (None, "", {}):
        values = notesps.upd_vals.get()
    else:
        if notesps.parent_id.get() not in (None, ""):
            values["parent_id"] = notesps.parent_id.get()
        if view_id not in (None, "", 0):
            values["view_id"] = view_id
        if table_id not in (None, "", 0):
            values["table_id"] = table_id
        if col_id not in (None, ""):
            values["col_id"] = col_id
        if item_id not in (None, "", 0):
            values["item_id"] = item_id
        if notesps.note.get() not in (None, ""):
            values["note"] = notesps.note.get()
        if notesps.note_txt.get() not in (None, ""):
            values["note_txt"] = notesps.note_txt.get()
    if notes_id not in (None, "", 0, "0"):
        stmt = update(table_notes).where(table_notes.c.notes_id == notes_id).values(**values)
        DB.executeDBUpdate(stmt)
        # clear old notifications for this note_id and view_id
        notificaitons = DB.getTableMeta("sys_notificaitons")
        stmt = update(notificaitons).where(notificaitons.c.view_id == view_id).where(notificaitons.c.notes_id == notes_id).values(is_delete = 1)
        DB.executeDBUpdate(stmt)
    else:
        values["created_by"] = userps.user_id.get()
        values["created_date"] = formatDate(created_date, "%Y-%m-%d %H:%M:%S")
        stmt = insert(table_notes).values(**values)
        notes_id = DB.executeDBInsert(stmt)
    return notes_id

def getSmileyData(notesps):
    notes_id = int(notesps.notes_id.get() or 0)
    created_by = userps.user_id.get()
    if notesps.created_by.get() not in (None, "", 0):
        created_by = notesps.created_by.get()
    notes_smiley = DB.getTableMeta("sys_table_notes_smiley").alias("notes_smiley")
    stmt = (
        select(
            notes_smiley
        )
        .where(notes_smiley.c.notes_id == notes_id)
        .where(notes_smiley.c.created_by == created_by)
        .where(notes_smiley.c.is_delete == 0)
    )
    return DB.executeDBSelectSingle(stmt)

def insertUpdateEmoji(notesps):
    smiley_id = int(notesps.smiley_id.get() or 0)
    notes_id = int(notesps.notes_id.get() or 0)
    view_id = int(notesps.view_id.get() or 0)
    item_id = int(notesps.item_id.get() or 0)
    smiley_code = int(notesps.smiley_code.get() or 0)
    values = {}
    notes_smiley = DB.getTableMeta("sys_table_notes_smiley").alias("notes_smiley")
    if notesps.upd_vals.get() not in (None, {}):
        values = notesps.upd_vals.get()
    else:
        if notes_id not in (None, "", 0):
            values["notes_id"] = notes_id
        if view_id not in (None, "", 0):
            values["view_id"] = view_id
        if item_id not in (None, "", 0):
            values["item_id"] = item_id
        if smiley_code not in (None, "", 0):
            values["smiley_code"] = smiley_code
    if smiley_id not in (None, "", 0, "0"):
        stmt = update(notes_smiley).where(notes_smiley.c.smiley_id == smiley_id).values(**values)
        DB.executeDBUpdate(stmt)
    else:
        values["created_by"] = userps.user_id.get()
        values["created_date"] = nowWithTimeZone()
        stmt = insert(notes_smiley).values(**values)
        smiley_id = DB.executeDBInsert(stmt)
    return smiley_id