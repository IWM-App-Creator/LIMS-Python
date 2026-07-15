from app.utils.common import DB, select, insert, update, func, text, userps, nowWithTimeZone

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
    stmt = stmt.order_by(tblcols.c.rank.asc())
    return DB.executeDBSelect(stmt)

def insertTableDataToDB(dbps) :
    table_id = dbps.table_id.get()
    table_name = dbps.table_name.get()
    table_alias = dbps.table_alias.get()
    user_id = userps.user_id.get()
    tblmaster = DB.getTableMeta("sys_db_tables")
    stmt = (
        insert(tblmaster)
            .values(
                table_name = table_name,
                table_alias = table_alias,
                is_visible = 1,
                created_by = user_id,
                created_date = nowWithTimeZone()
            )
    )
    table_id = DB.executeDBInsert(stmt)
    dbps.table_id.set(table_id)
    return table_id

def updateTableData(dbps) :
    table_id = dbps.table_id.get()
    table_alias = dbps.table_alias.get()
    tblmaster = DB.getTableMeta("sys_db_tables")
    stmt = (
        update(tblmaster)
        .where(tblmaster.c.table_id == table_id)
        .values(
            table_alias = table_alias
        )
    )
    DB.executeDBUpdate(stmt)

def insertUpdateTable(dbps):
    table_id = dbps.table_id.get()
    # table_name = dbps.table_name.get()
    table_alias = dbps.table_alias.get()
    user_id = userps.user_id.get()
    values = {
        # "table_name": table_name,
        "table_alias": table_alias,
        "is_visible": 1,
        "created_by": user_id,
        "created_date": nowWithTimeZone()
    }
    values = {}
    if dbps.table_name.get() not in (None, ""):
        values["table_name"] = dbps.table_name.get()

    # if table_alias not in (None, ""):
    #     values["table_alias"] = table_alias

    # values["is_visible"] = 1  # Always include

    # if user_id not in (None, ""):
    #     values["created_by"] = user_id

    # values["created_date"] = nowWithTimeZone()  # Always include

    tblmaster = DB.getTableMeta("sys_db_tables")
    where_clause = (tblmaster.c.table_id == table_id)
    stmt = select(tblmaster.c.table_id).where(where_clause)
    row = DB.executeDBSelectSingle(stmt) # Check if record exists
    if row: # Update existing record
        stmt = (
            update(tblmaster)
            .where(where_clause)
            .values(**values)
        )
        DB.executeDBUpdate(stmt)
        table_id = row.table_id
    else :  # Insert new record
        stmt = insert(tblmaster).values(**values)
        table_id = DB.executeDBInsert(stmt)
    return table_id

def insertUpdateTblCol(dbps) :
    tblcols = DB.getTableMeta("sys_new_db_tables_cols")
    values = {}
    if dbps.table_id.get() not in (None, "", 0):
        values["table_id"] = dbps.table_id.get()
    if dbps.col_name.get() not in (None, ""):
        values["col_name"] = dbps.col_name.get()
    if dbps.col_alias.get() not in (None, ""):
        values["col_alias"] = dbps.col_alias.get()
    if dbps.col_options.get() not in (None, "", {}):
        values["col_options"] = dbps.col_options.get()
    if dbps.rank.get() not in (None, "", 0):
        values["rank"] = dbps.rank.get()
    # Check for Insert / Update
    col_id = dbps.col_id.get()
    if col_id not in (None, "", 0) : # Update existing record
        stmt = (
            update(tblcols)
            .where(tblcols.c.col_id == col_id)
            .values(**values)
        )
        print("stmt --> ", stmt)
        # DB.executeDBUpdate(stmt)
    else : # Insert new record
        values["created_by"] = userps.user_id.get() # Include Create By
        values["created_date"] = nowWithTimeZone() # Include Create Date
        stmt = insert(tblcols).values(**values)
        col_id = DB.executeDBInsert(stmt)
    dbps.col_id.set(col_id)

def getDBColData(dbps):
    table_id = dbps.table_id.get()
    table_ids = dbps.table_ids.get()
    col_id = dbps.col_id.get()
    col_ids = dbps.col_ids.get()
    col_name = dbps.col_name.get()
    is_primary = dbps.is_primary.get()
    is_del_col = dbps.is_del_col.get()
    # print("is_del_tbl --> ", is_del_tbl)
    # print("is_del_col --> ", is_del_col)
    tblcols = DB.getTableMeta("sys_new_db_tables_cols").alias("tblcols")
    stmt = (
        select(tblcols)
    )
    if table_id not in (None, "", 0):
        stmt = stmt.where(tblcols.c.table_id == table_id)
    if table_ids:
        stmt = stmt.where(tblcols.c.table_id.in_(table_ids))
    if col_id not in (None, "", 0):
        stmt = stmt.where(tblcols.c.col_id == col_id)
    if col_ids:
        stmt = stmt.where(tblcols.c.col_id.in_(col_ids))
    if col_name not in (None, ""):
        stmt = stmt.where(tblcols.c.col_name == col_name)
    if is_primary:
        stmt = stmt.where(func.json_unquote(func.json_extract(tblcols.c.col_options, "$.is_primary") ) == "1" )
    # if is_del_col != "-1":
    #     stmt = stmt.where(tblcols.c.is_delete == is_del_col)
    return DB.executeDBSelect(stmt)

def updateDBTableSequence(dbps):
    db_tbl_cols = DB.getTableMeta("sys_new_db_tables_cols")
    stmt = select(db_tbl_cols).where(db_tbl_cols.c.table_id == dbps.table_id.get()).where(db_tbl_cols.c.is_delete == 0).order_by(db_tbl_cols.c.rank.asc())
    rows = DB.executeDBSelect(stmt)
    rank = 10
    for row in rows:
        stmt = update(db_tbl_cols).where(db_tbl_cols.c.col_id == row.col_id).values(rank = rank)
        DB.executeDBUpdate(stmt)
        rank += 10