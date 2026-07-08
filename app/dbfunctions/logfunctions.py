from app.utils.common import select, DB, insert, delete, userps, nowWithTimeZone

def getDBErrorLog(error_id: str, section: str, item_id: str):
    tblerrorlog = DB.getTableMeta("sys_error_log").alias("errlog")
    tbluser = DB.getTableMeta("users", "systemconfig").alias("usr")
    tblview = DB.getTableMeta("sys_new_dynamic_view").alias("dyncv")
    stmt = (
        select(tblerrorlog, tbluser.c.first_name, tbluser.c.last_name, tblview.c.view_name, tblview.c.url)
        .select_from(
            tblerrorlog
            .outerjoin(
                tbluser,
                tblerrorlog.c.created_by == tbluser.c.id
            )
            .outerjoin(
                tblview,
                (tblerrorlog.c.section == "View") &
                (tblerrorlog.c.item_id == tblview.c.view_id)
            )
        )        
    )
    if section not in (None, "", 0):
        stmt = stmt.where(tblerrorlog.c.section == section)
    if item_id not in (None, "", 0):
        stmt = stmt.where(tblerrorlog.c.item_id == item_id)
    if error_id not in (None, "", 0):
        stmt = stmt.where(tblerrorlog.c.error_id == error_id)
    stmt = stmt.order_by(tblerrorlog.c.created_date.desc())
    return DB.executeDBSelect(stmt)

def saveErrorLogtoDB(section: str, item_id: str, notes: str, error_msg: str):
    sys_error_log = DB.getTableMeta("sys_error_log")
    stmt = (
        insert(sys_error_log)
        .values(
            section = section,
            item_id = item_id,
            notes = notes,
            error_msg = error_msg,
            created_by = userps.user_id.get(),
            created_date = nowWithTimeZone()
        )
    )
    error_id = DB.executeDBInsert(stmt)
    return error_id

def resolveError(error_id: str):
    sys_error_log = DB.getTableMeta("sys_error_log")
    stmt = ( delete(sys_error_log).where(sys_error_log.c.error_id == error_id) )
    DB.executeDBDelete(stmt)