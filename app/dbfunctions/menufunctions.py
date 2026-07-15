from app.utils.common import select, update, insert, or_, DB, userps, nowWithTimeZone

def getMenuCentreData(menups):
    dync_menu_centre = DB.getTableMeta("sys_dynamic_menu_centre").alias("dmc")
    stmt = select(dync_menu_centre)
    if menups.m_centre_id.get() not in (None, "", 0):
        stmt = stmt.where(dync_menu_centre.c.m_centre_id == menups.m_centre_id.get())
    if menups.is_public.get() not in (None, ""):
        stmt = stmt.where(dync_menu_centre.c.is_public == menups.is_public.get())
    if menups.is_active.get() not in (None, ""):
        stmt = stmt.where(dync_menu_centre.c.is_active == menups.is_active.get())
    if menups.created_by.get() not in (None, "", 0):
        stmt = stmt.where(dync_menu_centre.c.created_by == menups.created_by.get())
    if menups.m_centre_ids.get() not in (None, [], ""):
        stmt = stmt.where(
            or_(
                dync_menu_centre.c.m_centre_id.in_(menups.m_centre_ids.get()),
                dync_menu_centre.c.is_public == 1,
                dync_menu_centre.c.created_by == userps.user_id.get()
            )
        )
    stmt = stmt.where(dync_menu_centre.c.is_delete == 0)
    stmt = stmt.order_by(dync_menu_centre.c.m_centre_id.asc())
    stmt = stmt.distinct()
    return DB.executeDBSelect(stmt)

def insertUpdateMenuCentre(menups):
    dync_menu_centre = DB.getTableMeta("sys_dynamic_menu_centre")
    values = {}
    if menups.centre_name not in (None, ""):
        values["centre_name"] = menups.centre_name.get()
    if menups.menu_json not in (None, []):
        values["menu_json"] = menups.menu_json.get()
    if menups.short_desc not in (None, ""):
        values["short_desc"] = menups.short_desc.get()
    if menups.preview_img not in (None, ""):
        values["preview_img"] = menups.preview_img.get()
    if menups.is_public not in (None, ""):
        values["is_public"] = menups.is_public.get()
    if menups.is_active not in (None, ""):
        values["is_active"] = menups.is_active.get()
    if menups.created_by not in (None, ""):
        values["created_by"] = menups.created_by.get()
    if menups.m_centre_id not in (None, "", 0):
        stmt = (
            update(dync_menu_centre)
            .where(dync_menu_centre.c.m_centre_id == menups.m_centre_id.get())
            .values(**values)
        )
        DB.executeDBUpdate(stmt)
    else:
        values["created_by"] = userps.user_id.get()
        values["created_date"] = nowWithTimeZone()
        stmt = (
            insert(dync_menu_centre)
            .values(**values)
        )
        m_centre_id = DB.executeDBInsert(stmt)
        menups.m_centre_id.set(m_centre_id)