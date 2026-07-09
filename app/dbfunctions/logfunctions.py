from app.utils.common import DB, select, insert, delete, func, userps, nowWithTimeZone

def getDBErrorLog(logps):
    page_no = logps.page_no.get()
    error_id = logps.error_id.get()
    section = logps.section.get()
    item_id = logps.item_id.get()
    page_size = logps.page_size.get()
    page_no = max(1, int(page_no))
    offset = (page_no - 1) * page_size
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
    # Create count statement from the existing statement
    count_stmt = stmt.with_only_columns(func.count()).order_by(None)
    logps.total_record.set(DB.executeDBScalar(count_stmt))
    # Apply paging to the original statement
    stmt = (
        stmt.order_by(tblerrorlog.c.created_date.desc())
            .limit(page_size)
            .offset(offset)
    )
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