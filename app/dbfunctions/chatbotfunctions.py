from app.utils.common import DB, select, insert, update, func, exists, and_, case, literal, nowWithTimeZone, userps

def getUserCBMdFromDB():
    cbusrmd = DB.getTableMeta("sys_cb_user_module").alias("cbusrmd")
    cblibmd = DB.getTableMeta("cb_lib_modules").alias("cblibmd")
    stmt = (
        select(cbusrmd, cblibmd.c.module_name, cblibmd.c.module_icon)
        .outerjoin(cblibmd, cblibmd.c.cb_lib_module_id == cbusrmd.c.cb_lib_module_id)
        .where(
            cbusrmd.c.is_delete == 0,
            cbusrmd.c.created_by == userps.user_id.get()
        )
    )
    return DB.executeDBSelect(stmt)


def insertUserCBMD():
    cbusrmd = DB.getTableMeta("sys_cb_user_module").alias("cbusrmd")
    stmt = (
        insert(cbusrmd)
        .values(
            cb_lib_module_id = 1,
            rank = 10,
            is_delete = 0,
            created_by = userps.user_id.get(),
            created_date = nowWithTimeZone()
        )
    )
    cb_user_module_id = DB.executeDBInsert(stmt)
    return cb_user_module_id
