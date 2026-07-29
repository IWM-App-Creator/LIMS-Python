import datetime
from app.utils.common import DB, select, or_, func, and_, userps

def getNotes(notesps):
    print("getNotes --> ")
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