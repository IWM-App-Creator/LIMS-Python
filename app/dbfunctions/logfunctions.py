from app.functions.datetime import now
from sqlalchemy import insert, delete
from app.utils.common import  DB, userps

from app.properties.logproperties import logps

def saveErrorLog ():
    sys_error_log = DB.getTableMeta("sys_error_log").alias("errlog")
    stmt = (
        insert(sys_error_log)
        .values(
            type = logps.log_type.get(),
            view_id = logps.view_id.get(),
            section = logps.section.get(),
            desc = logps.desc.get(),
            error_msg = logps.error_msg.get(),
            created_by = userps.user_id.get(),
            created_date = now()
        )
    )
    return DB.executeDBInsert(stmt)

def resolveError():
    error_id = logps.error_id.get(),
    sys_error_log = DB.getTableMeta("sys_error_log").alias("errlog")
    stmt = (
        delete(sys_error_log)
        .where(sys_error_log.c.error_id == error_id)
    )
    DB.executeDBDelete(stmt)