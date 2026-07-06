from sqlalchemy import func
from app.utils.common import select, DB
# from app.properties.usersproperties import userps
# from app.properties.dbproperties import dbps

def getDBTableData(dbps):
    table_id = dbps.table_id.get()
    table_ids = dbps.table_ids.get()
    col_id = dbps.col_id.get()
    col_ids = dbps.col_ids.get()
    table_name = dbps.table_name.get()
    col_name = dbps.col_name.get()
    is_primary = dbps.is_primary.get()
    is_del_tbl = dbps.is_del_tbl.get()
    is_del_col = dbps.is_del_col.get()
    # print("is_del_tbl --> ", is_del_tbl)
    # print("is_del_col --> ", is_del_col)
    tblcols = DB.getTableMeta("sys_new_db_tables_cols").alias("tblcols")
    tblmaster = DB.getTableMeta("sys_db_tables").alias("tbl")
    stmt = (
        select(
            tblcols,
            tblmaster.c.table_name,
            tblmaster.c.table_alias
        )
        .select_from(
            tblcols.outerjoin (
                tblmaster,
                tblmaster.c.table_id == tblcols.c.table_id
            )
        )
    )
    stmt = stmt.where(tblmaster.c.table_name.not_like("sys_%"))
    if table_id not in (None, "", 0):
        stmt = stmt.where(tblcols.c.table_id == table_id)
    if table_ids:
        stmt = stmt.where(tblcols.c.table_id.in_(table_ids))
    if col_id not in (None, "", 0):
        stmt = stmt.where(tblcols.c.col_id == col_id)
    if col_ids:
        stmt = stmt.where(tblcols.c.col_id.in_(col_ids))
    if table_name not in (None, ""):
        stmt = stmt.where(tblmaster.c.table_name == table_name)
    if col_name not in (None, ""):
        stmt = stmt.where(tblcols.c.col_name == col_name)
    if is_primary:
        stmt = stmt.where( func.json_unquote( func.json_extract(tblcols.c.col_options, "$.is_primary") ) == "1" )
    if is_del_tbl != "-1":
        stmt = stmt.where(tblmaster.c.is_delete == is_del_tbl)
    if is_del_col != "-1":
        stmt = stmt.where(tblcols.c.is_delete == is_del_col)
    # print("stmt --> ", stmt)
    return DB.executeDBSelect(stmt)