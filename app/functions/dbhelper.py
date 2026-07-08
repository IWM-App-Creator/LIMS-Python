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
