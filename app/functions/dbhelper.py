from app.functions.generalfunctions import addUpdateJson

# def updateViewCol(view_json: dict, col_id: int, **updates):
#     for col in view_json.get("view_cols", []):
#         if col.get("col_id") == col_id:
#             col.update(updates)
#             return True
#     return False
# updateViewCol(data, 3255, colkey=2)

# def insertViewColAfter(view_json: dict, after_col_id: int, new_col: dict):
#     for i, col in enumerate(view_json.get("view_cols", [])):
#         if col.get("col_id") == after_col_id:
#             view_json["view_cols"].insert(i + 1, new_col)
#             return True
#     return False
# insertViewColAfter(data, 3255, new_col)

# def insertViewColBefore(view_json: dict, before_col_id: int, new_col: dict):
#     for i, col in enumerate(view_json.get("view_cols", [])):
#         if col.get("col_id") == before_col_id:
#             view_json["view_cols"].insert(i, new_col)
#             return True
#     return False
# insertViewColBefore(data, 3255, new_col)

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
    if length not in ("", 0):
        tmpsql = tmpsql + " (" + length + ")"
    if is_primary == 1:
        tmpsql = tmpsql + " NOT NULL AUTO_INCREMENT"
    else : 
        tmpsql = tmpsql + " NULL"
    if default_val != "":
        tmpsql = tmpsql + " DEFAULT " + default_val
    colqry.append(tmpsql)
    if is_index == 1:
        colindex.append(f"INDEX `{col_name}` (`{col_name}` ASC)")
    # Set To Property
    dbps.colsql.set(colqry)
    dbps.colindex.set(colindex)

def prepareCreateQueryFromCols():
    print("prepareCreateQueryFromCols")
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

# def setQueryColStmt():
#     print("setQueryColStatement")

def getPrimaryColParam(table_id, col_name, col_alias, rank):
    colopt = {"table_id": table_id, "col_name": col_name, "col_alias": col_alias, "col_options": {"data_type": "bigint", "length": "11", "default_val": "", "is_primary": 1, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "rank": rank}, "view_cols": {"col_id": "", "col_name": col_name, "col_alias": col_alias, "col_type": "NUMBER", "qry_alias": "mtbl", "col_key": 1, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 0, "lookup_colnm": "", "rank": rank} }
    return colopt

def getStatusColParam(table_id, col_alias, cnt, rank):
    col_name = "status_" + cnt
    colopt = {"table_id": table_id, "col_name": col_name, "col_alias": col_alias, "col_options": {"data_type": "int", "length": "4", "default_val": "0", "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "rank": rank}, "view_cols": {"col_id": "", "col_name": col_name, "col_alias": col_alias, "col_type": "STATUS", "qry_alias": "mtbl", "col_key": 0, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 0, "lookup_colnm": "", "rank": rank} }
    return colopt

def getDropdownColParam(col_alias, cnt, rank):
    col_name = "dd_" + cnt
    colopt = {"col_name": col_name, "col_alias": col_alias, "data_type": "text", "length": 0, "default_val": "", "is_primary": 0, "is_index": 0, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "col_type": "DROPDOWN", "col_key": 0, "rank": rank }
    return colopt

def getYesNoColParam(col_alias, cnt, rank):
    col_name = "yn_" + cnt
    colopt = {"col_name": col_name, "col_alias": col_alias, "data_type": "int", "length": 4, "default_val": 0, "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": [{"label": "YES", "clrcode": "#10b759", "opt_val": "1"}, {"label": "NO", "clrcode": "#c66565", "opt_val": "2"}, {"label": "Unassigned", "clrcode": "#d2d2d2", "opt_val": "0"}], "col_type": "YN_INT", "col_key": 0, "rank": rank }
    return colopt

def getTrueFalseColParam(col_alias, cnt, rank):
    col_name = "tf_" + cnt
    colopt = {"col_name": col_name, "col_alias": col_alias, "data_type": "int", "length": 4, "default_val": 0, "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": [{"label": "True", "clrcode": "#10b759", "opt_val": "1"}, {"label": "False", "clrcode": "#c66565", "opt_val": "2"}, {"label": "Unassigned", "clrcode": "#d2d2d2", "opt_val": "0"}], "col_type": "YN_INT", "col_key": 0, "rank": rank }
    return colopt

def getPeopleColParam(col_alias, cnt, notify_user, rank):
    col_name = "ppl_" + cnt
    colopt = {"col_name": col_name, "col_alias": col_alias, "data_type": "varchar", "length": 250, "default_val": 0, "is_primary": 0, "is_index": 0, "is_unique": 0, "is_mandatory": 0, "notify_user": notify_user, "col_data_items": "", "col_type": "FULLNAME", "col_key": 0, "rank": rank }
    return colopt

# NUMBER, FLOAT(DECIMAL), GEO LOCATION

# Text, URL, EMAIL, TEL, UPLOAD, FORMULA, SIGN, BARCODE

# DATE & LAST UPDATE

# Float : {"length": "10,3", "is_index": 1, "data_type": "float", "is_unique": 0, "is_primary": 0, "default_val": null, "notify_user": 0, "csv_col_name": null, "csv_col_type": null, "is_mandatory": 0, "actv_log_cols": 0, "csv_map_col_nm": null}
  
def getIsDeleteColParam(rank):
    colopt = {"col_name": "is_delete", "col_alias": "ID Deleted", "data_type": "int", "length": 1, "default_val": 0, "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 1, "col_data_items": "", "col_type": "DEL_INT", "col_key": 0, "rank": rank }
    return colopt

def getIsMetadataColParam(rank):
    colopt = {"col_name": "is_metadata", "col_alias": "Metadata", "data_type": "json", "length": 0, "default_val": 0, "is_primary": 0, "is_index": 0, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "col_type": "META_DATA", "col_key": 0, "rank": rank }
    return colopt

def getCreatedByColParam(rank):
    colopt = {"col_name": "created_by", "col_alias": "Created By", "data_type": "bigint", "length": 11, "default_val": 0, "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "col_type": "FULLNAME", "col_key": 0, "rank": rank }
    return colopt

def getCreatedDateColParam(rank):
    colopt = {"col_name": "created_date", "col_alias": "Created Date", "data_type": "datetime", "length": 0, "default_val": 0, "is_primary": 0, "is_index": 0, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "col_type": "DATETIME", "col_key": 0, "rank": rank }
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
