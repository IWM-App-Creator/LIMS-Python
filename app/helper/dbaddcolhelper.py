from app.utils.common import Request, JSONResponse, RequestData, raiseAPIError, DB, text
from app.helper import dbhelper as dbhlp
from app.helper.generalfunctions import updateNestedJsonVal

def getColumnParams(dbps):
    if dbps.default_val.get() == "":
        dbps.is_null.set(1)
    colopt = {}
    match dbps.view_col_type.get():
        case "Status":
            colopt = dbhlp.getStatusColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.col_cnt.get(), dbps.rank.get())
            if dbps.default_val.get() == "":
                dbps.default_val.set(0)
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
        case "DDL":
            colopt = dbhlp.getDropdownColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.col_cnt.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
        case "YesNo":
            colopt = dbhlp.getYesNoColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.col_cnt.get(), dbps.rank.get())
            if dbps.default_val.get() == "":
                dbps.default_val.set(0)
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
        case "TrueFalse":
            colopt = dbhlp.getTrueFalseColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.col_cnt.get(), dbps.rank.get())
            if dbps.default_val.get() == "":
                dbps.default_val.set(0)
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
        case "People/Assign To":
            colopt = dbhlp.getPeopleColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.col_cnt.get(), dbps.notify_user.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
        case "Calc":
            colopt = dbhlp.getCalculationColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.col_cnt.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= None, srchval = None, updkey = "calc_formula", updval = dbps.calc_formula.get())
        case "Rating":
            colopt = dbhlp.getRatingColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.col_cnt.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= None, srchval = None, updkey = "calc_formula", updval = dbps.calc_formula.get())
        case "Barcode":
            colopt = dbhlp.getBarcodeColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.col_cnt.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "length", updval = 255)
        case "Sign":
            colopt = dbhlp.getSignatureColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.col_cnt.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "length", updval = 255)
        case "Geolocation":
            colopt = dbhlp.getGeolocationColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.col_cnt.get(), dbps.rank.get())
        case "Numbers":
            colopt = dbhlp.getNumberColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.rank.get())
            if dbps.is_index.get() == "":
                dbps.is_index.set(0)
            if dbps.length.get() == "":
                dbps.length.set(0)
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "data_type", updval = dbps.data_type.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "is_index", updval = dbps.is_index.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "length", updval = dbps.length.get())
        case "Text":
            colopt = dbhlp.getTextColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "data_type", updval = dbps.data_type.get())
            if dbps.data_type.get() == "varchar":
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "length", updval = dbps.length.get())
        case "URL":
            colopt = dbhlp.getTextColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "length", updval = 255)
            updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= None, srchval = None, updkey = "url_prefix", updval = dbps.url_prefix.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= None, srchval = None, updkey = "link_text", updval = dbps.link_text.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= None, srchval = None, updkey = "col_type", updval = "URL")
        case "Email":
            colopt = dbhlp.getTextColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= None, srchval = None, updkey = "col_type", updval = "EMAIL")
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "length", updval = 45)
        case "Tel":
            colopt = dbhlp.getTextColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= None, srchval = None, updkey = "col_type", updval = "TEL")
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "length", updval = 45)
        case "Colour":
            colopt = dbhlp.getTextColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= None, srchval = None, updkey = "col_type", updval = "COLOUR")
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "length", updval = 45)
        case "Upload":
            colopt = dbhlp.getTextColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= None, srchval = None, updkey = "col_type", updval = "UPLOAD")
            updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "length", updval = 300)
        case "Date":
            colopt = dbhlp.getDateColParam(dbps.table_id.get(), dbps.col_alias.get(), dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= None, srchval = None, updkey = "date_format", updval = dbps.date_format.get())
        case "LastUpdated":
            colopt = dbhlp.getDateColParam(dbps.table_id.get(), "Last Updated", dbps.rank.get())
            updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= None, srchval = None, updkey = "date_format", updval = dbps.date_format.get())
    return colopt