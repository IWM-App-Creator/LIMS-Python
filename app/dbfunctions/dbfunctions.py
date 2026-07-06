from sqlalchemy import text
from app.utils.common import select, DB, userps
import re

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

def generateDBColumnAlterQuery(dbps):
    schema_name = userps.schema_name.get()
    table_name = dbps.table_name.get()
    col_name = dbps.col_name.get()
    to_col_name = dbps.to_col_name.get()
    after_col = dbps.after_col.get()
    datatype = dbps.datatype.get()
    length = dbps.length.get()
    if length not in (None, ""):
        datatype = f"{datatype}({length})"

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
                f"`{datatype}` NULL "
                f"DEFAULT `{default_clause}` "
                f"AFTER `{after_clause}`;"
            )

        case "change_col":
            alter_qry = (
                f"ALTER TABLE `{schema_name}`.`{table_name}` "
                f"CHANGE COLUMN `{col_name}` "
                f"`{to_col_name}` "
                f"`{datatype}` NULL "
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

def getDBTables():
    print("getDBTables --> ")
    user_id = userps.user_id.get() # Get User ID
    # Prepare Query
    tbluser = DB.tableMeta("users").alias("usr")
    stmt = select(tbluser)
    if user_id not in (None, ""):
        stmt = stmt.where(tbluser.c.id == user_id)
    user = DB.executeDBSelectSingle(stmt) # Execute Query
    return user