from app.utils.common import DB, select, insert, update, func, userps, nowWithTimeZone

def getViewDataByID(viewps):
    view_id = viewps.view_id.get()
    tblview = DB.getTableMeta("sys_new_dynamic_view").alias("dyncv")
    stmt = (select(tblview)).where(tblview.c.is_delete == 0)
    is_single = 0
    if view_id not in (None, "", 0):
        stmt = stmt.where(tblview.c.view_id == view_id)
        is_single = 1
    if is_single == 1 : # Return Single Value 
        userview = DB.executeDBSelectSingle(stmt)
    else : # Return Array Value 
        userview = DB.executeDBSelect(stmt)
    viewps.userview.set(userview)

def insertUpdateView(viewps) :
    tblview = DB.getTableMeta("sys_new_dynamic_view")
    values = {}
    # print("view_name --> ", viewps.view_name.get())
    # print("view_name --> ", viewps.view_name.get())
    # print("view_url --> ", viewps.view_url.get())
    # print("view_type --> ", viewps.view_type.get())
    # print("view_options --> ", viewps.view_options.get())
    # print("view_cols --> ", viewps.view_cols.get())
    # print("view_joins --> ", viewps.view_joins.get())
    
    if viewps.view_name.get() not in (None, ""):
        values["view_name"] = viewps.view_name.get()
    if viewps.view_url.get() not in (None, ""):
        values["url"] = viewps.view_url.get()
    if viewps.view_type.get() not in (None, ""):
        values["view_type"] = viewps.view_type.get()
    if viewps.view_options.get() not in (None, "", []):
        values["view_options"] = viewps.view_options.get()
    if viewps.view_cols.get() not in (None, "", []):
        values["view_cols"] = viewps.view_cols.get()
    if viewps.view_joins.get() not in (None, "", []):
        values["view_joins"] = viewps.view_joins.get()
    if viewps.view_child.get() not in (None, "", []):
        values["view_child"] = viewps.view_child.get()
    if viewps.view_actions.get() not in (None, "", []):
        values["view_actions"] = viewps.view_actions.get()
    if viewps.dync_cat_id.get() not in (None, ""):
        values["dync_cat_id"] = viewps.dync_cat_id.get()
    if viewps.short_desc.get() not in (None, ""):
        values["short_desc"] = viewps.short_desc.get()
    if viewps.preview_img.get() not in (None, ""):
        values["preview_img"] = viewps.preview_img.get()
    if viewps.is_delete.get() not in (None, ""):
        values["is_delete"] = viewps.is_delete.get()
    # Check for Insert / Update
    view_id = viewps.view_id.get()
    if view_id not in (None, "0", ""): # Update existing record
        stmt = (
            update(tblview)
            .where(tblview.c.view_id == view_id)
            .values(**values)
        )
        DB.executeDBUpdate(stmt)
    else : # Insert new record
        values["created_by"] = userps.user_id.get() # Include Create By
        values["created_date"] = nowWithTimeZone() # Include Create Date
        stmt = insert(tblview).values(**values)
        # print("stmt --> ", stmt)
        view_id = DB.executeDBInsert(stmt)
    viewps.view_id.set(view_id)

