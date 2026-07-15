from app.utils.common import select, update, insert, or_, DB, userps, nowWithTimeZone

def getMenuCentreData(menups):
    dync_menu_centre = DB.getTableMeta("sys_dynamic_menu_centre").alias("dmc")
    stmt = select(dync_menu_centre)
    if menups.m_centre_id.get() not in (None, "", 0):
        stmt = stmt.where(dync_menu_centre.c.m_centre_id == menups.m_centre_id.get())
    if menups.is_public.get() not in (None, "", 0):
        stmt = stmt.where(dync_menu_centre.c.is_public == menups.is_public.get())
    if menups.is_active.get() not in (None, "", 0):
        stmt = stmt.where(dync_menu_centre.c.is_active == menups.is_active.get())
    if menups.created_by.get() not in (None, "", 0):
        stmt = stmt.where(dync_menu_centre.c.created_by == menups.created_by.get())
    stmt = stmt.where(dync_menu_centre.c.is_delete == 0)
    return DB.executeDBSelect(stmt)