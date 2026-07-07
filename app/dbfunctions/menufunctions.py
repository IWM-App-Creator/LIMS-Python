from app.utils.common import select, DB, JSONResponse, raiseAPIError, userps
from app.properties.menuproperties import menups

def getDynamicMenu():
    dync_menu = DB.getTableMeta("sys_dynamic_menu").alias("sdm")
    stmt = (
        select(dync_menu)
    )
    if menups.m_centre_id.get() not in (None, "", 0):
        stmt = stmt.where(dync_menu.c.m_centre_id == menups.m_centre_id.get())
    stmt = stmt.where(dync_menu.c.created_by == userps.user_id.get())
    stmt = stmt.where(dync_menu.c.is_delete == 0)
    return DB.executeDBSelect(stmt)

def getDynamicMenuCenter():
    dync_menu_cntr = DB.getTableMeta('sys_dynamic_menu_centre').alias('sdmc')
    stmt = (
        select(dync_menu_cntr)
    )
    if menups.m_centre_id.get() not in (None, "", 0):
        stmt = stmt.where(dync_menu_cntr.c.m_centre_id == menups.m_centre_id.get())
    if menups.is_public.get() not in (None, "", 0):
        stmt = stmt.where(dync_menu_cntr.c.is_public == menups.is_public.get())
    if menups.is_active.get() not in (None, "", 0):
        stmt = stmt.where(dync_menu_cntr.c.is_active == menups.is_active.get())
    stmt = stmt.where(dync_menu_cntr.c.created_by == userps.user_id.get())
    stmt = stmt.where(dync_menu_cntr.c.is_delete == 0)
    return DB.executeDBSelect(stmt)

def getUserMenuList():
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
    return DB.executeDBSelect(stmt)