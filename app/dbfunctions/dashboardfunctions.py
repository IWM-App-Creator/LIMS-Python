from app.utils.common import select, update, insert, or_, DB, userps, nowWithTimeZone

def getDashboardData(dps):
    schema_name = dps.schema_name.get()
    dashboard_id = int(dps.dashboard_id.get() or 0)
    user_id = int(dps.created_by.get() or 0)
    dashboard = DB.getTableMeta("sys_user_dashboard", schema_name).alias("ud")
    stmt = (
        select(dashboard)
        .where(dashboard.c.is_delete == 0)
    )
    if dashboard_id not in (None, "", 0):
        stmt = stmt.where(dashboard.c.dashboard_id == dashboard_id)
        return DB.executeDBSelectSingle(stmt)
    if dps.created_by.get() not in (None, "", 0):
        stmt = stmt.where(dashboard.c.created_by == user_id)
    return DB.executeDBSelect(stmt)

def insertUpdateDashboard(dps) :
    dashboard = DB.getTableMeta("sys_user_dashboard")
    user_id = int(userps.user_id.get() or 0)
    if dps.created_by.get() not in (None, "", 0):
        user_id = int(dps.created_by.get() or 0)
    values = {}
    db_upd_vals = dps.db_upd_vals.get() 
    if db_upd_vals is not None :
       values = db_upd_vals
    else :
        if dps.dashboard_name.get() not in (None, ""):
            values["dashboard_name"] = dps.dashboard_name.get()
        if dps.is_active.get() not in (None, ""):
            values["is_active"] = dps.is_active.get()
    # if is active then inactive all
    if dps.is_active.get() in (1, "1"):
        stmt = update(dashboard).where(dashboard.c.created_by == user_id).values({"is_active": 0})
        DB.executeDBUpdate(stmt)
    # Check for Insert / Update
    dashboard_id = int(dps.dashboard_id.get() or 0)
    if dashboard_id not in (None, 0, ""): # Update Existing Record
        stmt = (
            update(dashboard)
            .where(dashboard.c.dashboard_id == dashboard_id)
            .values(**values)
        )
        DB.executeDBUpdate(stmt)
    else : # Insert new record
        values["created_by"] = user_id # Include Create By
        values["created_date"] = nowWithTimeZone() # Include Create Date
        stmt = insert(dashboard).values(**values)
        dashboard_id = DB.executeDBInsert(stmt)
    dps.dashboard_id.set(dashboard_id)
