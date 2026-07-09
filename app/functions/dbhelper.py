from app.functions.generalfunctions import addUpdateJson

def setColOptions(dbps):
    col_options = {}
    addUpdateJson(col_options, "length", dbps.length.get())
    addUpdateJson(col_options, "is_index", dbps.is_index.get())
    addUpdateJson(col_options, "datatype", dbps.datatype.get())
    addUpdateJson(col_options, "is_unique", dbps.is_unique.get())
    addUpdateJson(col_options, "is_primary", dbps.is_primary.get())
    addUpdateJson(col_options, "default_val", dbps.default_val.get())
    addUpdateJson(col_options, "notify_user", dbps.notify_user.get())
    addUpdateJson(col_options, "is_mandatory", dbps.is_mandatory.get())
    addUpdateJson(col_options, "actv_log_cols", dbps.actv_log_cols.get())
    addUpdateJson(col_options, "col_data_items", dbps.col_data_items.get())
    dbps.col_options.set(col_options)

def getPrimaryColParam(col_name, col_alias, rank):
    colopt = {"col_name": col_name, "col_alias": col_alias, "data_type": "bigint", "length": 11, "default_val": 0, "is_primary": 1, "is_index": 1, "is_unique": 0, "is_mandatory": 1, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "col_type": "NUMBER", "colkey": 1, "rank": rank }
    return colopt

def getStatusColParam(col_alias, cnt, rank):
    col_name = "status_" + cnt
    colopt = {"col_name": col_name, "col_alias": col_alias, "data_type": "int", "length": 4, "default_val": 0, "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "col_type": "STATUS", "colkey": 0, "rank": rank }
    return colopt

def getDropdownColParam(col_alias, cnt, rank):
    col_name = "dd_" + cnt
    colopt = {"col_name": col_name, "col_alias": col_alias, "data_type": "text", "length": 0, "default_val": "", "is_primary": 0, "is_index": 0, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "col_type": "DROPDOWN", "colkey": 0, "rank": rank }
    return colopt

def getYesNoColParam(col_alias, cnt, rank):
    col_name = "yn_" + cnt
    colopt = {"col_name": col_name, "col_alias": col_alias, "data_type": "int", "length": 4, "default_val": 0, "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": [{"label": "YES", "clrcode": "#10b759", "opt_val": "1"}, {"label": "NO", "clrcode": "#c66565", "opt_val": "2"}, {"label": "Unassigned", "clrcode": "#d2d2d2", "opt_val": "0"}], "col_type": "YN_INT", "colkey": 0, "rank": rank }
    return colopt

def getTrueFalseColParam(col_alias, cnt, rank):
    col_name = "tf_" + cnt
    colopt = {"col_name": col_name, "col_alias": col_alias, "data_type": "int", "length": 4, "default_val": 0, "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": [{"label": "True", "clrcode": "#10b759", "opt_val": "1"}, {"label": "False", "clrcode": "#c66565", "opt_val": "2"}, {"label": "Unassigned", "clrcode": "#d2d2d2", "opt_val": "0"}], "col_type": "YN_INT", "colkey": 0, "rank": rank }
    return colopt

def getPeopleColParam(col_alias, cnt, notify_user, rank):
    col_name = "ppl_" + cnt
    colopt = {"col_name": col_name, "col_alias": col_alias, "data_type": "varchar", "length": 250, "default_val": 0, "is_primary": 0, "is_index": 0, "is_unique": 0, "is_mandatory": 0, "notify_user": notify_user, "col_data_items": "", "col_type": "FULLNAME", "colkey": 0, "rank": rank }
    return colopt

# NUMBER, FLOAT(DECIMAL), GEO LOCATION

# Text, URL, EMAIL, TEL, UPLOAD, FORMULA, SIGN, BARCODE

# DATE & LAST UPDATE

# Float : {"length": "10,3", "is_index": 1, "data_type": "float", "is_unique": 0, "is_primary": 0, "default_val": null, "notify_user": 0, "csv_col_name": null, "csv_col_type": null, "is_mandatory": 0, "actv_log_cols": 0, "csv_map_col_nm": null}
  
def getIsDeleteColParam(rank):
    colopt = {"col_name": "is_delete", "col_alias": "ID Deleted", "data_type": "int", "length": 1, "default_val": 0, "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 1, "col_data_items": "", "col_type": "DEL_INT", "colkey": 0, "rank": rank }
    return colopt

def getIsMetadataColParam(rank):
    colopt = {"col_name": "is_metadata", "col_alias": "Metadata", "data_type": "json", "length": 0, "default_val": 0, "is_primary": 0, "is_index": 0, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "col_type": "META_DATA", "colkey": 0, "rank": rank }
    return colopt

def getCreatedByColParam(rank):
    colopt = {"col_name": "created_by", "col_alias": "Created By", "data_type": "bigint", "length": 11, "default_val": 0, "is_primary": 0, "is_index": 1, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "col_type": "FULLNAME", "colkey": 0, "rank": rank }
    return colopt

def getCreatedDateColParam(rank):
    colopt = {"col_name": "created_date", "col_alias": "Created Date", "data_type": "datetime", "length": 0, "default_val": 0, "is_primary": 0, "is_index": 0, "is_unique": 0, "is_mandatory": 0, "notify_user": 0, "actv_log_cols": 0, "col_data_items": "", "col_type": "DATETIME", "colkey": 0, "rank": rank }
    return colopt


def isStatusColumn(colname: str) -> bool:
    return colname.startswith("status_")

def isDDColumn(colname: str) -> bool:
    return colname.startswith(("dd_", "dync_"))

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
