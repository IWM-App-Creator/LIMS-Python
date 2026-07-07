from app.utils.common import select, DB, JSONResponse, raiseAPIError, userps

def getDynamicMenu(menups):
    m_centre_id = menups.m_centre_id.get()
    created_by = menups.created_by.get()
    fetch_single = menups.fetch_single.get()

    dync_menu = DB.getTableMeta("sys_dynamic_menu").alias("sdm")
    stmt = (
        select(dync_menu)
    )
    if m_centre_id not in (None, "", 0):
        stmt = stmt.where(dync_menu.c.m_centre_id == m_centre_id)
    if created_by not in (None, "", 0):
        stmt = stmt.where(dync_menu.c.created_by == created_by)
    stmt = stmt.where(dync_menu.c.is_delete == 0)
    if fetch_single == 1 :
        return DB.executeDBSelectSingle(stmt)
    else :
        return DB.executeDBSelect(stmt)

def getDynamicMenuCenter(menups):
    m_centre_id = menups.m_centre_id.get()
    is_active = menups.is_active.get()
    is_public = menups.is_public.get()
    created_by = menups.created_by.get()
    fetch_single = menups.fetch_single.get()

    dync_menu_cntr = DB.getTableMeta('sys_dynamic_menu_centre').alias('sdmc')
    stmt = (select(dync_menu_cntr))
    if m_centre_id not in (None, "", 0):
        stmt = stmt.where(dync_menu_cntr.c.m_centre_id == m_centre_id)
    if is_active not in (None, ""):
        stmt = stmt.where(dync_menu_cntr.c.is_active == is_active)
    if is_public not in (None, ""):
        stmt = stmt.where(dync_menu_cntr.c.is_public == is_public)
    if created_by not in (None, "", 0):
        stmt = stmt.where(dync_menu_cntr.c.created_by == created_by)
    stmt = stmt.where(dync_menu_cntr.c.is_delete == 0)
    if fetch_single == 1 :
        return DB.executeDBSelectSingle(stmt)
    else :
        return DB.executeDBSelect(stmt)

def getUserMenuList(menups):
    fetch_single = menups.fetch_single.get()
    dync_menu = DB.getTableMeta("sys_dynamic_menu").alias("sdm")
    dync_view = DB.getTableMeta("sys_dynamic_view").alias("sdv")
    custom_view = DB.getTableMeta("sys_custom_view").alias("scv")
    stmt = (
        select(
            dync_menu,
            dync_view.c.url,
            custom_view.c.view_url,
        )
        .select_from(
            dync_menu
            .outerjoin(
                dync_view,
                dync_view.c.view_id == dync_menu.c.view_id
            )
            .outerjoin(
                custom_view,
                custom_view.c.custom_view_id == dync_menu.c.view_id
            )
        )
        .where(dync_menu.c.m_centre_id == menups.m_centre_id.get())
        .where(dync_menu.c.is_delete == 0)
    )
    if menups.usr_flag.get() in (None, "", 0):
        stmt = stmt.where(dync_menu.c.created_by == userps.user_id.get())
    stmt = stmt.order_by(dync_menu.c.rank.asc())
    if fetch_single == 1 :
        return DB.executeDBSelectSingle(stmt)
    else :
        return DB.executeDBSelect(stmt)