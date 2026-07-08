from sqlalchemy import select, func, text, insert, update, delete, or_
from app.dbhelper.db_helper import DB
from app.properties.usersproperties import userps
from app.functions.datetime import nowWithTimeZone

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