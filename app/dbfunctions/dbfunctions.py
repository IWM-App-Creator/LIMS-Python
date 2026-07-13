from app.utils.common import DB, select, text, userps
import re
# from sqlalchemy import inspect

def getDBTablesFromSchema(dbps):
    schema_name = userps.schema_name.get()
    # Get All Tables
    stmt = text(f"SHOW TABLES FROM `{schema_name}`")
    all_db_tables = DB.executeDBStatement(stmt)
    dbps.all_db_tables.set(all_db_tables) # Set To Properties

def getColFromTablesSchema(dbps):
    schema_name = userps.schema_name.get()
    table_name = dbps.table_name.get()
    stmt = text(f"DESCRIBE `{schema_name}`.`{table_name}`")
    all_db_tbl_col = DB.executeDBStatement(stmt)
    dbps.all_db_tbl_col.set(all_db_tbl_col) # Set To Properties

@staticmethod
def getTableColumnCount(dbps):
    getColFromTablesSchema(dbps) # Get Table Columns From DB
    tbl_col_cnt = 0
    tbl_col_srch = dbps.tbl_col_srch.get()
    columns = dbps.all_db_tbl_col.get()
    for col in columns:
        if col.Field.startswith(f"{tbl_col_srch}"):
            tbl_col_cnt = tbl_col_cnt + 1
    dbps.tbl_col_cnt.set(tbl_col_cnt)

def getCreateTableSqlFromSchema(dbps):
    schema_name = userps.schema_name.get()
    table_name = dbps.table_name.get()
    stmt = text(
        f"SHOW CREATE TABLE `{schema_name}`.`{table_name}`"
    )
    create = DB.executeDBStatement(stmt).first()
    sql_qry = ""
    if create :
        sql_qry = create._mapping["Create Table"]
        sql_qry = re.sub(
            r"AUTO_INCREMENT=\d+",
            "AUTO_INCREMENT=1",
            sql_qry,
            flags=re.IGNORECASE
        )
        sql_qry = sql_qry + ";\n\n"
    dbps.create_qry.set(sql_qry) # Set Query To Properties

def executeCreateQuery(table_id: int, table_name: str):
    # tblcols = DB.getTableMeta("sys_db_tables_cols")
    # stmt = (
    #     select(tblcols)
    #     .where(
    #         tblcols.c.table_id == table_id,
    #         tblcols.c.is_delete == 0
    #     )
    #     .order_by(tblcols.c.rank.asc())
    # )
    # dbtablecols = DB.executeDBSelect(stmt)
    # columns = []
    # indexes = []
    # primary = ""

    print(create_sql)
    
    for col in dbtablecols:
        col_name = col.col_name.lower()
        data_type = col.data_type.lower()
        if col.is_primary == 1:
            columns.append(
                f"`{col_name}` {data_type}({col.length}) NOT NULL AUTO_INCREMENT"
            )
            primary = f"PRIMARY KEY (`{col_name}`)"
            continue
        # Build datatype
        if data_type in ("datetime", "json", "text", "longtext", "tinytext"):
            datatype_sql = data_type.upper()
        else:
            datatype_sql = f"{data_type}({col.length})"
        sql = f"`{col_name}` {datatype_sql} NULL"
        # Default value
        if col.default_val not in (None, ""):
            if data_type in (
                "varchar",
                "text",
                "longtext",
                "tinytext",
                "datetime",
                "date",
                "timestamp",
            ):
                sql += f" DEFAULT '{col.default_val}'"
            else:
                sql += f" DEFAULT {col.default_val}"
        elif data_type in ("int", "bigint", "tinyint", "decimal", "float", "double"):
            sql += " DEFAULT 0"
        columns.append(sql)
        if col.is_index == 1 and data_type != "json":
            indexes.append(f"INDEX `{col_name}` (`{col_name}` ASC)")
    # create_sql = f"""
    # CREATE TABLE `{table_name}` (
    #     {", ".join(columns)}
    #     {"," if primary or indexes else ""}
    #     {primary}
    #     {"," if primary and indexes else ""}
    #     {", ".join(indexes)}
    # )
    # ENGINE=InnoDB
    # DEFAULT CHARSET=utf8
    # COLLATE=utf8_general_ci
    # AUTO_INCREMENT=1;
    # """
    # print(create_sql)
    # DB.executeDBStatement(text(create_sql))
    # # Convert text columns to utf8mb4
    # for col in dbtablecols:
    #     data_type = col.data_type.lower()
    #     if data_type in ("varchar", "text", "longtext", "tinytext"):
    #         if data_type == "varchar":
    #             datatype = f"VARCHAR({col.length})"
    #         else:
    #             datatype = data_type.upper()
    #         alter_sql = f"""
    #         ALTER TABLE `{table_name}`
    #         MODIFY `{col.col_name.lower()}`
    #         {datatype}
    #         CHARACTER SET utf8mb4
    #         COLLATE utf8mb4_unicode_ci;
    #         """
    #         DB.executeDBStatement(text(alter_sql))

def generateDBColumnAlterQuery(dbps):
    schema_name = userps.schema_name.get()
    table_name = dbps.table_name.get()
    col_name = dbps.col_name.get()
    to_col_name = dbps.to_col_name.get()
    after_col = dbps.after_col.get()
    data_type = dbps.data_type.get()
    length = dbps.length.get()
    if length not in (None, ""):
        data_type = f"{data_type}({length})"

    default_clause = ""
    default_val = dbps.default_val.get()
    if default_val not in (None, ""):
        default_clause = f" {default_val}"

    after_clause = ""
    if after_col not in (None, ""):
        after_clause = f"`{after_col}`"

    extra_clause = ""
    extra = dbps.extra.get()
    if extra:
        extra_clause = f" {extra}" # $qps->extra = "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;";

    alter_action = dbps.alter_action.get().lower()
    match alter_action:
        case "add_col":
            alter_qry = (
                f"ALTER TABLE `{schema_name}`.`{table_name}` "
                f"ADD COLUMN `{col_name}` "
                f"`{data_type}` NULL "
                f"DEFAULT `{default_clause}` "
                f"AFTER `{after_clause}`;"
            )

        case "change_col":
            alter_qry = (
                f"ALTER TABLE `{schema_name}`.`{table_name}` "
                f"CHANGE COLUMN `{col_name}` "
                f"`{to_col_name}` "
                f"`{data_type}` NULL "
                f"DEFAULT `{default_clause}`;"
            )

        case "drop_col":
            alter_qry = (
                f"ALTER TABLE `{schema_name}`.`{table_name}` "
                f"DROP COLUMN `{col_name}`;"
            )

        case "add_unique_col":
            alter_qry = (
                f"ALTER TABLE `{schema_name}`.`{table_name}` "
                f"ADD UNIQUE (`{col_name}`) "
                f"`{extra_clause}`;"
            )

        case "remove_unique_col":
            alter_qry = (
                f"ALTER TABLE `{schema_name}`.`{table_name}` "
                f"ADD UNIQUE (`{col_name}`) "
                f"`{extra_clause}`;"
            )

        case "set_auto_increment":
            alter_qry = (
                f"ALTER TABLE `{schema_name}`.`{table_name}` "
                f"AUTO_INCREMENT = {int(extra)};"
            )
        case _:
            alter_qry = ""
    dbps.alter_qry.set(alter_qry)

def makeColumnUnique(dbps):
    col_name = dbps.col_name.get()
    getColFromTablesSchema()
    all_db_tbl_col = dbps.all_db_tbl_col.get()
    is_found = 0
    for col in all_db_tbl_col:
        if col.Field == col_name and col.Key == "UNI":
            is_found = 1

    if is_found == 0:
        dbps.alter_action.set("add_unique_col")
        alter_qry = generateDBColumnAlterQuery(dbps)
        DB.executeDBStatement(text(alter_qry))

def removeColumnUnique(dbps):
    col_name = dbps.col_name.get()
    getColFromTablesSchema()
    all_db_tbl_col = dbps.all_db_tbl_col.get()
    is_found = 0
    for col in all_db_tbl_col:
        if col.Field == col_name and col.Key == "UNI":
            is_found = 1
    if is_found == 1:
        dbps.alter_action.set("remove_unique_col")
        alter_qry = generateDBColumnAlterQuery(dbps)
        DB.executeDBStatement(text(alter_qry))
