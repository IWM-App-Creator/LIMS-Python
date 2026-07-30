import datetime
from app.utils.common import DB, select, or_, func, and_, userps, nowWithTimeZone

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