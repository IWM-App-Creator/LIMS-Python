from app.utils.common import select, update, insert, or_, DB, userps, nowWithTimeZone

def getCustomViewData(customvwps):
    schema_name = customvwps.schema_name.get()
    custom_view = DB.getTableMeta("sys_custom_view", schema_name).alias("cv")
    stmt = select(custom_view)
    stmt = stmt.where(custom_view.c.is_delete == 0).order_by(custom_view.c.view_name.asc())
    return DB.executeDBSelect(stmt)

def addUpdateCustomView(customvwps):
    custom_view = DB.getTableMeta("sys_custom_view")
    where_clause = (custom_view.c.custom_view_id == customvwps.custom_view_id.get())
    stmt = select(custom_view.c.custom_view_id).where(where_clause)
    values = {}
    if customvwps.view_name.get() not in (None, "", 0):
        values["view_name"] = customvwps.view_name.get()
    if customvwps.view_url.get() not in (None, "", 0):
        values["view_url"] = customvwps.view_url.get()
    if customvwps.dync_cat_id.get() not in (None, "", 0):
        values["dync_cat_id"] = customvwps.dync_cat_id.get()
    if customvwps.short_desc.get() not in (None, "", 0):
        values["short_desc"] = customvwps.short_desc.get()
    if customvwps.preview_img.get() not in (None, "", 0):
        values["preview_img"] = customvwps.preview_img.get()
    if customvwps.status_1.get() not in (None, "", 0):
        values["status_1"] = customvwps.status_1.get()
    if customvwps.is_delete.get() not in (None, "", 0):
        values["is_delete"] = customvwps.is_delete.get()
    row = DB.executeDBSelectSingle(stmt) # Check if record exists
    if row: # Update existing record
        stmt = (
            update(custom_view)
            .where(where_clause)
            .values(**values)
        )
        DB.executeDBUpdate(stmt)
        custom_view_id = row.custom_view_id
    else :  # Insert new record
        values["created_by"] = userps.user_id.get()
        values["created_date"] = nowWithTimeZone()
        stmt = insert(custom_view).values(**values)
        custom_view_id = DB.executeDBInsert(stmt)
    return custom_view_id