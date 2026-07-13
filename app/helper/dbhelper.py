from app.utils.common import DB
from app.dbfunctions.dbfunctions import getTableColumnCount
from app.dbfunctions.dbtablesfunctions import getDBTableData

def setQueryColStmt(dbps):
    colqry = dbps.colsql.get()
    colindex = dbps.colindex.get()
    col_name = dbps.col_name.get()
    col_options = dbps.col_options.get()
    data_type = col_options.get("data_type")
    length = col_options.get("length")
    default_val = col_options.get("default_val")
    is_primary = col_options.get("is_primary")
    is_index = col_options.get("is_index")
    # Prepare Col Query
    tmpsql = col_name + " " + data_type
    if length not in ("", "0", 0):
        tmpsql = tmpsql + " (" + length + ")"
    if is_primary == 1: # Col Primary
        tmpsql = tmpsql + " NOT NULL AUTO_INCREMENT"
        dbps.colprimary.set("PRIMARY KEY (`" + col_name + "`)") # Col Primary
    else : 
        tmpsql = tmpsql + " NULL"
    if default_val != "":
        tmpsql = tmpsql + " DEFAULT " + default_val
    if data_type in ("varchar", "text", "longtext", "tinytext"):
       tmpsql = tmpsql + " CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    colqry.append(tmpsql)
    if is_index == 1: # Col Index
        colindex.append(f"INDEX `{col_name}` (`{col_name}` ASC)")
    # Set To Property
    dbps.colsql.set(colqry)
    dbps.colindex.set(colindex)

def executeCreateTableQuery(dbps):
    table_name = dbps.table_name.get()
    colqry = dbps.colsql.get() or []
    colprimary = dbps.colprimary.get() or ""
    indexes = dbps.colindex.get() or []
    sql_parts = colqry.copy()
    if colprimary:
        sql_parts.append(colprimary)
    if indexes:
        sql_parts.extend(indexes)
    create_sql = f"""
    CREATE TABLE `{table_name}` (
        {", ".join(sql_parts)}
    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8
    COLLATE=utf8_general_ci
    AUTO_INCREMENT=1;
    """
    print("executeCreateTableQuery create_sql --> ", create_sql)
    DB.executeDBStatement(create_sql)

def getPrimaryColParam(table_id, col_name, col_alias, rank):
    colopt = {"table_id": table_id, "col_name": col_name, "col_alias": col_alias, "col_options": {"data_type": "bigint", "length": "11", "default_val": "", "is_primary": 1, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "rank": rank}, "view_cols": {"col_id": "", "col_name": col_name, "col_alias": col_alias, "col_type": "NUMBER", "qry_alias": "mtbl", "col_key": 1, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 0, "lookup_colnm": "", "rank": rank} }
    return colopt

def getStatusColParam(table_id, col_alias, cnt, rank):
    col_name = "status_" + str(cnt)
    colopt = {"table_id": table_id, "col_name": col_name, "col_alias": col_alias, "col_options": {"data_type": "int", "length": "4", "default_val": "0", "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "rank": rank}, "view_cols": {"col_id": "", "col_name": col_name, "col_alias": col_alias, "col_type": "STATUS", "qry_alias": "mtbl", "col_key": 0, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 0, "lookup_colnm": "", "rank": rank} }
    return colopt

def getDropdownColParam(table_id, col_alias, cnt, rank):
    col_name = "dd_" + str(cnt)
    colopt = {"table_id": table_id, "col_name": col_name, "col_alias": col_alias, "col_options": {"data_type": "text", "length": "", "default_val": "", "is_primary": 0, "is_index": 0, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "rank": rank}, "view_cols": {"col_id": "", "col_name": col_name, "col_alias": col_alias, "col_type": "DROPDOWN", "qry_alias": "mtbl", "col_key": 0, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 0, "lookup_colnm": "", "rank": rank} }
    return colopt

def getYesNoColParam(table_id, col_alias, cnt, rank):
    col_name = "yn_" + str(cnt)
    colopt = {"table_id": table_id, "col_name": col_name, "col_alias": col_alias, "col_options": {"data_type": "int", "length": "4", "default_val": "0", "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": [{"label": "YES", "clrcode": "#10b759", "opt_val": "1"}, {"label": "NO", "clrcode": "#c66565", "opt_val": "2"}, {"label": "Unassigned", "clrcode": "#d2d2d2", "opt_val": "0"}], "rank": rank}, "view_cols": {"col_id": "", "col_name": col_name, "col_alias": col_alias, "col_type": "YN_INT", "qry_alias": "mtbl", "col_key": 0, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 0, "lookup_colnm": "", "rank": rank} }
    return colopt

def getTrueFalseColParam(table_id, col_alias, cnt, rank):
    col_name = "tf_" + str(cnt)
    colopt = {"table_id": table_id, "col_name": col_name, "col_alias": col_alias, "col_options": {"data_type": "int", "length": "4", "default_val": "0", "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": [{"label": "True", "clrcode": "#10b759", "opt_val": "1"}, {"label": "False", "clrcode": "#c66565", "opt_val": "2"}, {"label": "Unassigned", "clrcode": "#d2d2d2", "opt_val": "0"}], "rank": rank}, "view_cols": {"col_id": "", "col_name": col_name, "col_alias": col_alias, "col_type": "TF_INT", "qry_alias": "mtbl", "col_key": 0, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 0, "lookup_colnm": "", "rank": rank} }
    return colopt

def getPeopleColParam(table_id, col_alias, cnt, notify_user, rank):
    col_name = "ppl_" + str(cnt)
    colopt = {"table_id": table_id, "col_name": col_name, "col_alias": col_alias, "col_options": {"data_type": "varchar", "length": "250", "default_val": "", "is_primary": 0, "is_index": 0, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "rank": rank}, "view_cols": {"col_id": "", "col_name": col_name, "col_alias": col_alias, "col_type": "FULLNAME", "qry_alias": "mtbl", "col_key": 0, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 0, "lookup_colnm": "", "rank": rank} }
    return colopt

# NUMBER, FLOAT(DECIMAL), GEO LOCATION

# Text, URL, EMAIL, TEL, UPLOAD, FORMULA, SIGN, BARCODE

# DATE & LAST UPDATE

# Float : {"length": "10,3", "is_index": 1, "data_type": "float", "is_unique": 0, "is_primary": 0, "default_val": null, "notify_user": 0, "csv_col_name": null, "csv_col_type": null, "is_mandatory": 0, "actv_log_cols": 0, "csv_map_col_nm": null}
  
def getIsDeleteColParam(table_id, rank):
    colopt = {"table_id": table_id, "col_name": "is_delete", "col_alias": "ID Deleted", "col_options": {"data_type": "int", "length": "1", "default_val": "0", "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 1, "col_data_items": "", "rank": rank}, "view_cols": {"col_id": "", "col_name": "is_delete", "col_alias": "ID Deleted", "col_type": "DEL_INT", "qry_alias": "mtbl", "col_key": 0, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 0, "lookup_colnm": "", "rank": rank} }
    return colopt

def getIsMetadataColParam(table_id, rank):
    colopt = {"table_id": table_id, "col_name": "is_metadata", "col_alias": "Metadata", "col_options": {"data_type": "json", "length": "", "default_val": "", "is_primary": 0, "is_index": 0, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "rank": rank}, "view_cols": {"col_id": "", "col_name": "is_metadata", "col_alias": "Metadata", "col_type": "META_DATA", "qry_alias": "mtbl", "col_key": 0, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 0, "lookup_colnm": "", "rank": rank} }
    return colopt

def getCreatedByColParam(table_id, rank):
    colopt = {"table_id": table_id, "col_name": "created_by", "col_alias": "Created By", "col_options": {"data_type": "bigint", "length": "11", "default_val": "0", "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "rank": rank}, "view_cols": {"col_id": "", "col_name": "created_by", "col_alias": "Created By", "col_type": "FULLNAME", "qry_alias": "mtbl", "col_key": 2, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 492, "lookup_colnm": "", "rank": rank} }
    return colopt

def getCreatedDateColParam(table_id, rank):
    colopt = {"table_id": table_id, "col_name": "created_date", "col_alias": "Created Date", "col_options": {"data_type": "datetime", "length": "", "default_val": "", "is_primary": 0, "is_index": 0, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "rank": rank}, "view_cols": {"col_id": "", "col_name": "created_date", "col_alias": "Created Date", "col_type": "DATETIME", "qry_alias": "mtbl", "col_key": 0, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 0, "lookup_colnm": "", "rank": rank} }
    return colopt

def isStatusColumn(colname: str) -> bool:
    return colname.startswith("status_")

def isDDColumn(colname: str) -> bool:
    return colname.startswith("dd_")

def isPeopleColumn(colname: str) -> bool:
    return colname.startswith("ppl_")

def isTrueFalseColumn(colname: str) -> bool:
    return colname.startswith("tf_")

def isYesNoColumn(colname: str) -> bool:
    return colname.startswith("yn_")

def isCalcColumn(colname: str) -> bool:
    return colname.startswith("calc_")

def isUserColumn(colname: str, exclude_ppl: int = 0) -> bool:
    is_user = (
        colname.endswith("_by") or
        colname.endswith("user_id")
    )
    if not exclude_ppl:
        is_user = is_user or colname.startswith("ppl_")
    return is_user

def getViewCaseQuery(qrycolnm, col_name):
    qry = ""
    if isUserColumn(col_name, 0): # Single User
        qry = (
            f"CASE WHEN {qrycolnm} != '' THEN "
            f"(SELECT CONCAT(first_name, '**', last_name) "
            f"FROM systemconfig.users "
            f"WHERE users.id = {qrycolnm}) "
            f"ELSE '' END"
        )
    elif isPeopleColumn(col_name): # Multiple People
        qry = (
            f"CASE WHEN {qrycolnm} != '' THEN "
            f"(SELECT GROUP_CONCAT(CONCAT(first_name, '**', last_name) SEPARATOR ', ') "
            f"FROM systemconfig.users "
            f"WHERE FIND_IN_SET(users.id, {qrycolnm})) "
            f"ELSE '' END"
        )
    return qry

def getViewColumnCount(dbps):
    if dbps.view_col_type.get() in ("Status", "DDL", "YesNo", "TrueFalse", "People/Assign To", "Calc", "Rating", "Barcode", "Sign", "Geolocation") :
        match dbps.view_col_type.get():
            case "Status":
                dbps.tbl_col_srch.set("status_")
            case "DDL":
                dbps.tbl_col_srch.set("dd_")
            case "YesNo":
                dbps.tbl_col_srch.set("yn_")
            case "TrueFalse":
                dbps.tbl_col_srch.set("tf_")
            case "People/Assign To":
                dbps.tbl_col_srch.set("ppl_")
            case "Calc":
                dbps.tbl_col_srch.set("calc_")
            case "Rating":
                dbps.tbl_col_srch.set("rating_")
            case "Barcode":
                dbps.tbl_col_srch.set("barcode_")
            case "Sign":
                dbps.tbl_col_srch.set("sign_")
            case "Geolocation":
                dbps.tbl_col_srch.set("lat_")
        getTableColumnCount(dbps)

def setTableColumnRank(dbps):
    col_data = getDBTableData(dbps)
    print("setTableColumnRank col_data --> ", col_data)