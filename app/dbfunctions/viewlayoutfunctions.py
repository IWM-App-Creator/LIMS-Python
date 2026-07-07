from sqlalchemy import func
from app.utils.common import select, DB, userps

def getViewLayoutDataByID(viewps):
    view_id = viewps.view_id.get()
    user_id = userps.user_id.get()
    tblviewly = DB.getTableMeta("sys_view_layout_users").alias("viewly")
    stmt = (select(tblviewly))
    stmt = stmt.where(tblviewly.c.view_id == view_id)
    stmt = stmt.where(tblviewly.c.created_by == user_id)
    stmt = stmt.where(tblviewly.c.is_delete == 0)
    return DB.executeDBSelectSingle(stmt)
