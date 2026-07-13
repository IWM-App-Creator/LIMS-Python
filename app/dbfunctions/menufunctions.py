from app.utils.common import select, update, insert, or_, DB, userps, nowWithTimeZone

def getDynamicMenu(menups):
    m_centre_id = menups.m_centre_id.get()
    view_id = menups.view_id.get()
    m_type = menups.m_type.get()
    created_by = menups.created_by.get()
    fetch_single = menups.fetch_single.get()
    order_by = menups.order_by.get()
    order_type = menups.order_type.get()
    dync_menu = DB.getTableMeta("sys_dynamic_menu").alias("sdm")
    stmt = (
        select(dync_menu)
    )
    if m_centre_id not in (None, "", 0):
        stmt = stmt.where(dync_menu.c.m_centre_id == m_centre_id)
    if view_id not in (None, "", 0):
        stmt = stmt.where(dync_menu.c.view_id == view_id)
    if m_type not in (None, "", 0):
        stmt = stmt.where(dync_menu.c.m_type == m_type)
    if created_by not in (None, "", 0):
        stmt = stmt.where(dync_menu.c.created_by == created_by)
    if menups.is_delete.get() not in (None, ""):
        stmt = stmt.where(dync_menu.c.is_delete == menups.is_delete.get())
    if order_by not in (None, ""):
        if hasattr(dync_menu.c, order_by):
            column = getattr(dync_menu.c, order_by)
            if str(order_type).upper() == "DESC":
                stmt = stmt.order_by(column.desc())
            else:
                stmt = stmt.order_by(column.asc())
    if fetch_single == 1 :
        menups.menu_cntr_data.set(DB.executeDBSelectSingle(stmt))
    else :
        menups.menu_cntr_data.set(DB.executeDBSelect(stmt))

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
    if menups.is_delete.get() not in (None, ""):
        stmt = stmt.where(dync_menu_cntr.c.is_delete == menups.is_delete.get())
    if fetch_single == 1 :
        menups.menu_centre.set(DB.executeDBSelectSingle(stmt))
    else :
        menups.menu_centre.set(DB.executeDBSelect(stmt))

def getPublicOrUserMenuCenters(menups):
    dync_menu_cntr = DB.getTableMeta('sys_dynamic_menu_centre').alias('sdmc')
    stmt = (
        select(dync_menu_cntr)
        .where(
            or_(
                dync_menu_cntr.c.m_centre_id.in_(menups.m_centre_ids.get()),
                dync_menu_cntr.c.is_public == 1,
                dync_menu_cntr.c.created_by == userps.user_id.get()
            )
        )
        .where(dync_menu_cntr.c.is_delete == 0)
        .order_by(dync_menu_cntr.c.m_centre_id.asc())
        .distinct()
    )
    menups.menu_centre.set(DB.executeDBSelect(stmt))

def getUserMenuList(menups):
    created_by = menups.created_by.get()
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
    if menups.usr_flag.get() in (None, "", 0) and created_by not in (None, "", 0):
        stmt = stmt.where(dync_menu.c.created_by == created_by)
    stmt = stmt.order_by(dync_menu.c.rank.asc())
    menups.menu_cntr_data.set(DB.executeDBSelect(stmt))

def insertUpdateUserMenu(menups):
    menu_id = 0
    usermenu = DB.getTableMeta("sys_dynamic_menu")
    where_clause = (usermenu.c.menu_id == menups.menu_id.get())
    values = {}
    if menups.m_centre_id.get() not in (None, "", 0):
        values["m_centre_id"] = menups.m_centre_id.get()
    if menups.parent_menu_id.get() not in (None, ""):
        values["parent_menu_id"] = menups.parent_menu_id.get()
    if menups.is_section.get() not in (None, ""):
        values["is_section"] = menups.is_section.get()
    if menups.menu_name.get() not in (None, "", 0):
        values["menu_name"] = menups.menu_name.get()
    if menups.menu_url.get() not in (None, "", 0):
        values["menu_url"] = menups.menu_url.get()
    if menups.menu_icon.get() not in (None, "", 0):
        values["menu_icon"] = menups.menu_icon.get()
    if menups.menu_color.get() not in (None, "", 0):
        values["menu_color"] = menups.menu_color.get()
    if menups.m_type.get() not in (None, "", 0):
        values["m_type"] = menups.m_type.get()
    if menups.view_id.get() not in (None, "", 0):
        values["view_id"] = menups.view_id.get()
    if menups.is_new_tab.get() not in (None, ""):
        values["is_new_tab"] = menups.is_new_tab.get()
    if menups.is_custom_centre.get() not in (None, ""):
        values["is_custom_centre"] = menups.is_custom_centre.get()
    if menups.rank.get() not in (None, ""):
        values["rank"] = menups.rank.get()
    if menups.is_delete.get() not in (None, ""):
        values["is_delete"] = menups.is_delete.get()
    if menups.menu_id.get() not in (None, "", 0): # Update existing record
        stmt = (
            update(usermenu)
            .where(where_clause)
            .values(**values)
        )
        DB.executeDBUpdate(stmt)
        menu_id = menups.menu_id.get()
    else : # Insert new record
        values["created_by"] = userps.user_id.get()
        values["created_date"] = nowWithTimeZone()
        stmt = insert(usermenu).values(**values)
        menu_id = DB.executeDBInsert(stmt)
    menups.menu_id.set(menu_id)

def getDynamicMenuRank(menups):
    m_centre_id = menups.m_centre_id.get()
    created_by = menups.created_by.get()
    dync_menu = DB.getTableMeta("sys_dynamic_menu").alias("sdm")
    stmt = (
        select(dync_menu)
    )
    if m_centre_id not in (None, "", 0):
        stmt = stmt.where(dync_menu.c.m_centre_id == m_centre_id)
    if created_by not in (None, "", 0):
        stmt = stmt.where(dync_menu.c.created_by == created_by)
    stmt = stmt.order_by(dync_menu.c.rank.desc())
    last_rank = DB.executeDBSelectSingle(stmt)
    menups.last_menu_rank.set(last_rank.rank)