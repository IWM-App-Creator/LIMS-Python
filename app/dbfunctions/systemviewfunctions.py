from app.utils.common import select, DB, func, userps

def getSystemViewData(systemviewps):
    table_name = systemviewps.table_name.get() or ""
    page_no = int(systemviewps.page_no.get() or 1)
    page_size = int(systemviewps.page_size.get() or 5)
    sys_table = DB.getTableMeta(table_name, "geno").alias("table")
    stmt = (
        select(
            sys_table
        )
        .where(sys_table.c.is_delete == 0)
    )
    record_qry = select(func.count()).select_from(stmt.subquery())
    systemviewps.rcdcnt.set(DB.executeDBScalar(record_qry))
    offset = (page_no - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)
    return DB.executeDBSelect(stmt)