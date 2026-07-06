from sqlalchemy import func
from app.utils.common import select, DB

def getViewDataByID(viewps):
    view_id = viewps.view_id.get()
    tblview = DB.getTableMeta("sys_new_dynamic_view").alias("tblcols")
    stmt = (select(tblview)).where(tblview.c.is_delete == 0)
    if view_id not in (None, "", 0):
        stmt = stmt.where(tblview.c.view_id == view_id)
    return DB.executeDBSelect(stmt)