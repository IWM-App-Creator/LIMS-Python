from app.utils.common import select, DB, insert, delete, userps, nowWithTimeZone

def getErrorLog(error_id: int, section: str, item_id: str):
    tblerrorlog = DB.getTableMeta("sys_error_log").alias("errlog")
    stmt = (select(tblerrorlog))
    # error_id, section, item_id, notes, error_msg, created_by, created_date
    if section not in (None, "", 0):
        stmt = stmt.where(tblerrorlog.c.section == section)
        stmt = stmt.where(tblerrorlog.c.item_id == item_id)
    if error_id not in (None, "", 0):
        stmt = stmt.where(tblerrorlog.c.error_id == error_id)
    return DB.executeDBSelect(stmt)

def saveErrorLog(section: str, item_id: str, notes: str, error_msg: str):
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

def resolveError(error_id):
    sys_error_log = DB.getTableMeta("sys_error_log")
    stmt = ( delete(sys_error_log).where(sys_error_log.c.error_id == error_id) )
    DB.executeDBDelete(stmt)