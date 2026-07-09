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

def setColOptions(dbps):
    blnkvcol = dbps.blnkvcol.get()
    col_options = {}
    addUpdateJson(col_options, "data_type",  blnkvcol.get("data_type"))
    addUpdateJson(col_options, "length",  blnkvcol.get("length"))
    addUpdateJson(col_options, "default_val",  blnkvcol.get("default_val"))
    addUpdateJson(col_options, "is_primary",  blnkvcol.get("is_primary"))
    addUpdateJson(col_options, "is_index",  blnkvcol.get("is_index"))
    addUpdateJson(col_options, "is_unique",  blnkvcol.get("is_unique"))
    addUpdateJson(col_options, "is_mandatory",  blnkvcol.get("is_mandatory"))
    addUpdateJson(col_options, "notify_user",  blnkvcol.get("notify_user"))
    addUpdateJson(col_options, "actv_log_cols",  blnkvcol.get("actv_log_cols"))
    addUpdateJson(col_options, "col_data_items",  blnkvcol.get("col_data_items"))
    dbps.col_options.set(col_options)

def getPrimaryColParam(col_name, col_alias, rank):
    colopt = {"col_name": col_name, "col_alias": col_alias, "data_type": "bigint", "length": 11, "default_val": 0, "is_primary": 1, "is_index": 1, "is_unique": 0, "is_mandatory": 1, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "col_type": "NUMBER", "col_key": 1, "rank": rank }
    # "col_options": {"length": "11", "is_index": 0, "data_type": "bigint", "is_unique": 0, "is_primary": 1, "default_val": "0", "notify_user": 0, "is_mandatory": 0, "actv_log_cols": 0}
    return colopt

def getStatusColParam(col_alias, cnt, rank):
    col_name = "status_" + cnt
    colopt = {"col_name": col_name, "col_alias": col_alias, "data_type": "int", "length": 4, "default_val": 0, "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "col_type": "STATUS", "col_key": 0, "rank": rank }
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
