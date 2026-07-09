from app.utils.common import select, update, insert, or_, DB, userps, nowWithTimeZone

def getUserDashboards(dps):
    user_dashboard = DB.getTableMeta("sys_user_dashboard").alias("ud")
    stmt = (
        select(
            user_dashboard
        )
        .where(user_dashboard.c.is_delete == 0)
        .where(user_dashboard.c.created_by == userps.user_id.get())
    )
    if dps.fetch_single.get() == 1:
        dps.dashboards_data.set(DB.executeDBSelectSingle(stmt))
    else:
        dps.dashboards_data.set(DB.executeDBSelect(stmt))