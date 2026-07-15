from app.utils.common import select, update, insert, or_, DB, userps, nowWithTimeZone

def getDashboardData(dps):
    dashboard = DB.getTableMeta("sys_user_dashboard").alias("ud")
    stmt = (
        select(dashboard)
        .where(dashboard.c.is_delete == 0)
        .where(dashboard.c.created_by == userps.user_id.get())
    )
    return DB.executeDBSelect(stmt)

def insertUpdateDashboard(dps) :
    dashboard = DB.getTableMeta("sys_user_dashboard").alias("ud")
    values = {}
    db_upd_vals = dps.db_upd_vals.get() 
    # dashboard_id, dashboard_name, is_active, is_delete, created_by, created_date
    if db_upd_vals is not None :
       values = db_upd_vals
    else :
        if dps.dashboard_name.get() not in (None, ""):
            values["dashboard_name"] = dps.dashboard_name.get()
        if dps.is_active.get() not in (None, ""):
            values["is_active"] = dps.is_active.get()
    # Check for Insert / Update
    dashboard_id = dps.dashboard_id.get()
    if dashboard_id not in (None, 0, ""): # Update Existing Record
        stmt = (
            update(dashboard)
            .where(dashboard.c.dashboard_id == dashboard_id)
            .values(**values)
        )
        print("stmt --> ", stmt)
        # DB.executeDBUpdate(stmt)
    else : # Insert new record
        values["created_by"] = userps.user_id.get() # Include Create By
        values["created_date"] = nowWithTimeZone() # Include Create Date
        stmt = insert(dashboard).values(**values)
        print("stmt --> ", stmt)
        # workspace_id = DB.executeDBInsert(stmt)
    dps.dashboard_id.set(dashboard_id)
