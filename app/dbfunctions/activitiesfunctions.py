from app.utils.common import DB, select, or_, func, and_

def getActivityLogs(activitiesps):
    print("getActivityLog --> ")
    activity_logs = DB.getTableMeta("sys_activity_logs").alias("al")
    db_tbl_cols = DB.getTableMeta("sys_db_tables_cols").alias("dbtc")
    users = DB.getTableMeta("users", "systemconfig").alias("u")
    select_cols = [
        activity_logs,
        db_tbl_cols.c.col_name,
        db_tbl_cols.c.col_alias,
        func.concat(
            users.c.first_name,
            "**",
            users.c.last_name
        ).label("updatedby"),
    ]
    if activitiesps.viewflag.get() in (1, "1"):
        dync_view = DB.getTableMeta("sys_dynamic_view").alias("dv")
        select_cols.append(dync_view.c.view_name)
    stmt = (
        select(*select_cols)
        .outerjoin(
            db_tbl_cols,
            db_tbl_cols.c.col_id == activity_logs.c.col_id,
        )
        .outerjoin(
            users,
            users.c.id == activity_logs.c.updated_by,
        )
    )
    if activitiesps.viewflag.get() in (1, "1"):
        tableids = activitiesps.tableids.get()
        if isinstance(tableids, str):
            tableids = [tableids]
        stmt = (
            stmt.outerjoin(
                dync_view,
                dync_view.c.view_id == activity_logs.c.data_id,
            )
        )
        if tableids:
            stmt = stmt.where(activity_logs.c.table_id.in_(tableids))
    if activitiesps.data_id.get() not in (None, "", 0) and activitiesps.viewflag.get() not in (1, "1"):
        stmt = stmt.where(activity_logs.c.data_id == activitiesps.data_id.get())
    if activitiesps.item_id.get() not in (None, "", 0):
        stmt = stmt.where(activity_logs.c.item_id == activitiesps.item_id.get())
    if activitiesps.logtype.get() not in (None, ""):
        stmt = stmt.where(activity_logs.c.logtype == activitiesps.logtype.get())
    stmt = stmt.order_by(activity_logs.c.log_id.desc())
    return DB.executeDBSelect(stmt)

def getActivityLogById(activitiesps):
    log_id = int(activitiesps.log_id.get() or 0)
    activity_logs  = DB.getTableMeta("sys_activity_logs").alias("al")
    stmt = select(activity_logs).where(activity_logs.c.log_id == log_id)
    return DB.executeDBSelect(stmt)