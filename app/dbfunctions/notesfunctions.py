import datetime
from app.utils.common import DB, select, or_, func, and_, userps

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
            tbl_notes.c.created_date <= datetime.datetime.now(),
            tbl_notes.c.created_by == userps.user_id.get()
        )
    )
    stmt = stmt.order_by(tbl_notes.c.notes_id.asc())
    return DB.executeDBSelect(stmt)

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