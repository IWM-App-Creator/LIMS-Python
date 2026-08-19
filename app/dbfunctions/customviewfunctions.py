from app.utils.common import select, update, insert, or_, DB, userps, nowWithTimeZone

def getCustomViewData(customvwps):
    schema_name = customvwps.schema_name.get()
    custom_view = DB.getTableMeta("sys_custom_view", schema_name).alias("cv")
    stmt = select(custom_view)
    stmt = stmt.where(custom_view.c.is_delete == 0).order_by(custom_view.c.view_name.asc())
    return DB.executeDBSelect(stmt)

def addUpdateCustomView(customvwps):
    custom_view = DB.getTableMeta("sys_custom_view")
    custom_view_id = int(customvwps.custom_view_id.get() or 0)
    view_name = customvwps.view_name.get()
    view_url = customvwps.view_url.get()
    values = {}
    if customvwps.db_upd_vals.get() not in (None, "", {}):
        values = customvwps.db_upd_vals.get()
    else:
        if view_name not in (None, ""):
            values["view_name"] = view_name
        if view_url not in (None, ""):
            values["view_url"] = view_url
    if custom_view_id not in (None, "", 0):
        stmt = update(custom_view).where(custom_view.c.custom_view_id == custom_view_id).values(**values)
        DB.executeDBUpdate(stmt)
    else:
        values["created_by"] = userps.user_id.get()
        values["created_date"] = nowWithTimeZone()
        stmt = insert(custom_view).values(**values)
        custom_view_id = DB.executeDBInsert(stmt)
    customvwps.custom_view_id.set(custom_view_id)