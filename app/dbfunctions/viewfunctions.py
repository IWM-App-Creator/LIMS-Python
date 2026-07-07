from sqlalchemy import func
from app.utils.common import select, DB

def getViewDataByID(viewps):
    view_id = viewps.view_id.get()
    tblview = DB.getTableMeta("sys_new_dynamic_view").alias("tblcols")
    stmt = (select(tblview)).where(tblview.c.is_delete == 0)
    is_single = 0
    if view_id not in (None, "", 0):
        stmt = stmt.where(tblview.c.view_id == view_id)
        is_single = 1
    if is_single == 1 : # Return Single Value 
        return DB.executeDBSelectSingle(stmt)
    else : # Return Array Value 
        return DB.executeDBSelect(stmt)