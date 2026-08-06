from app.utils.common import select, DB, userps

def getSystemViewData(systemviewps):
    table_name = systemviewps.table_name.get() or ""
    schema_name = None
    if systemviewps.schema_name.get() not in (None, ""):
        schema_name = systemviewps.schema_name.get()
    sys_table = DB.getTableMeta(table_name, schema_name).alias("table")
    stmt = (
        select(
            sys_table
        )
        .where(sys_table.c.is_delete == 0)
    )
    return DB.executeDBSelect(stmt)