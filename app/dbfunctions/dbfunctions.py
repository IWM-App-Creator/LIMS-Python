from app.utils.common import DB, select, text, userps
import re
from sqlalchemy import inspect

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
        # print(dict(col._mapping))
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


# type_map = {
#     "DDL": "dd",
#     "People/Assign To": "ppl",
#     "YesNo": "yn",
#     "TrueFalse": "tf",
#     "Geolocation": "lat"
# }

# public function getColumnCount($rlps) {
#         $columns = DB::select('describe ' . $rlps->table_name);
#         $rlps->col_cnt = 0;
#         if($rlps->col_type == "DDL") {
#             $rlps->col_type = "dd";
#         } else if($rlps->col_type == "People/Assign To") {
#             $rlps->col_type = "ppl";
#         } else if($rlps->col_type == "YesNo") {
#             $rlps->col_type = "yn";
#         } else if($rlps->col_type == "TrueFalse") {
#             $rlps->col_type = "tf";
#         } else if($rlps->col_type == "Geolocation") {
#             $rlps->col_type = "lat";
#         }
#         foreach ($columns as $col) {
#             if($col->Field == "is_delete") {
#                 $rlps->previous_col = $rlps->tmp_col;
#             }
#             $rlps->tmp_col = $col->Field;
#             if($col->Field == $rlps->col_name) {
#                 $rlps->fetch_flag = 2;
#                 $rlps->error_msg = "Column already exists, Duplicate column name " . $rlps->col_name;
#                 break;
#             }
#             if (str_contains($col->Field, strtolower($rlps->col_type) . "_")) {
#                 $rlps->col_cnt = $rlps->col_cnt + 1;
#             }
#         }
#         $rlps->col_name = strtolower($rlps->col_type) . "_" . ($rlps->col_cnt + 1);
#     }

# if (str_contains($col->Field, 'status')) {
#         $statuscnt = $statuscnt + 1;
#     }
#     if (str_contains($col->Field, 'ppl_')) {
#         $usercnt = $usercnt + 1;
#     }
#     if (str_contains($col->Field, 'dd_')) {
#         $ddlcnt = $ddlcnt + 1;
#     }
#     if (str_contains($col->Field, 'yn_')) {
#         $yesnocnt = $yesnocnt + 1;
#     }
#     if (str_contains($col->Field, 'tf_')) {
#         $turefalsecnt = $turefalsecnt + 1;
#     }
#     if (str_contains($col->Field, 'lat_')) {
#         $latcnt = $latcnt + 1;
#     }
#     if (str_contains($col->Field, 'calc_')) {
#         $calccnt = $calccnt + 1;
#     }
#     if (str_contains($col->Field, 'rating_')) {
#         $ratingcnt = $ratingcnt + 1;
#     }
#     if (str_contains($col->Field, 'barcode_')) {
#         $barcodecnt = $barcodecnt + 1;
#     }
#     if (str_contains($col->Field, 'sign_')) {
#         $signcnt = $signcnt + 1;
#     }
# if($txtcol_dval == "" && ($txt_data_type == "int" || $txt_data_type == "bigint" || $txt_data_type == "float" || $txt_data_type == "decimal" || $txt_data_type == "double") ) {
