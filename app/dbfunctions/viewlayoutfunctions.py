from app.utils.common import select, DB, insert, update, nowWithTimeZone, and_, userps


def getViewLayoutDataByID(viewps):
    view_id = viewps.view_id.get()
    user_id = userps.user_id.get()
    tblviewly = DB.getTableMeta("sys_view_layout_users").alias("viewly")
    stmt = (select(tblviewly))
    stmt = stmt.where(tblviewly.c.view_id == view_id)
    stmt = stmt.where(tblviewly.c.created_by == user_id)
    stmt = stmt.where(tblviewly.c.is_delete == 0)
    return DB.executeDBSelectSingle(stmt)

def insertUpdateUserLayout(viewlyps):
    tbl_layout = DB.getTableMeta("sys_view_layout_users")
    srno = int(viewlyps.srno.get() or 0)
    view_id = int(viewlyps.view_id.get() or 0)
    values = {}
    if viewlyps.db_upd_vals.get() not in (None, {}):
        values = viewlyps.db_upd_vals.get()
    else:
        if srno not in (None, "", 0):
            values["srno"] = srno
        if view_id not in (None, "", 0):
            values["view_id"] = view_id
    if srno not in (None, "", 0, "0"):
        stmt = update(tbl_layout).where(tbl_layout.c.srno == srno).values(**values)
        DB.executeDBUpdate(stmt)
    else:
        values["created_by"] = userps.user_id.get()
        values["created_date"] = nowWithTimeZone()
        stmt = insert(tbl_layout).values(**values)
        srno = DB.executeDBInsert(stmt)
    print("stmt --> ", stmt)
    return srno