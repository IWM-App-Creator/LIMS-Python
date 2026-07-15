from app.utils.common import select, update, insert, or_, DB, userps, nowWithTimeZone

def getDashboardData(dps):
    user_dashboard = DB.getTableMeta("sys_user_dashboard").alias("ud")
    stmt = (
        select(
            user_dashboard
        )
        .where(user_dashboard.c.is_delete == 0)
        .where(user_dashboard.c.created_by == userps.user_id.get())
    )
    return DB.executeDBSelect(stmt)