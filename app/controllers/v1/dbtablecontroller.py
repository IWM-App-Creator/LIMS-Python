from app.utils.common import Request, JSONResponse, RequestData, raiseAPIError, DB, text
from app.dbfunctions.dbtablesfunctions import getDBTableData, insertTableDataToDB, insertUpdateTblCol, updateDBTableSequence
from app.helper.dbhelper import setQueryColStmt, executeCreateTableQuery
from app.dbfunctions.viewfunctions import getViewDataByID, insertUpdateView
from app.dbfunctions.dbfunctions import generateDBColumnAlterQuery
from app.helper.viewhelper import viewhlp
from app.helper import dbhelper as dbhlp
from app.properties.dbproperties import dbps
from app.properties.viewproperties import viewps
from app.helper.generalfunctions import sortObjectsByKey, generateRandomString, addUpdateJson, updateNestedJsonVal, insertNestedJsonAfter, insertNestedJsonBefore, removeNestedJsonVal, getHostName

# http://testws1.localhost:8000/api/v1/dbtable/gettbls
def getDBTableList (request: Request):
    # $user_id = empty(Input::get('user_id')) ? "1" : Input::get('user_id');
    #     $api_secret = empty(Input::get('api_secret')) ? "" : Input::get('api_secret');
    #     $excl_tbl_id = empty(Input::get('excl_tbl_id')) ? "" : Input::get('excl_tbl_id');
    #     $workspace_id = empty(Input::get('workspace_id')) ? "0" : Input::get('workspace_id');
    #     $flag = empty(Input::get('flag')) ? "" : Input::get('flag');
    #     $excl_tbl_id = explode(",", $excl_tbl_id);
    #     $excl_tbl_id = array_unique($excl_tbl_id);
    flag = ""
    tablesarr = getDBTableData(dbps) # Execute Function to User Get Data
    table_data = []
    for table in tablesarr:
        row = {
            "table_id": table.table_id,
            "table_name": table.table_name,
            "table_alias": table.table_alias
        }
        if flag == "DynamicView":
            row["col_alias"] = table.col_alias
        table_data.append(row)
    # Output
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "Table Data",
            "table_data": table_data
        }
    )

# http://testws1.localhost:8000/api/v1/dbtable/getcols
def getDBTableColumns (request: Request):
    print("getDBTableList --> ")

# http://testws1.localhost:8000/api/v1/dbtable/updatetbl
def updateDBTableAlias (request: Request):
    print("updateDBTableAlias --> ")

# http://testws1.localhost:8000/api/v1/dbtable/addcol?view_id=181&all_usr_flg=1&view_col_type=Numbers&col_alias=Decimal Col&default_val=&orderflag=left&ordercol_id=3302&notify_user=0&data_type=decimal&length=10,8&is_index=
def addDynamicColumn(request: Request):
    print("addDynamicColumn --> ")
    status = False
    message = "Invalid Request"
    try:
        params = RequestData.params(request)
        viewps.view_id.set(params.get("view_id", 0))
        dbps.col_alias.set(params.get("col_alias", ""))
        orderflag = params.get("orderflag", "Right")
        ordercol_id = params.get("ordercol_id", 0)
        notify_user = params.get("notify_user", 0)
        dbps.data_type.set(params.get("data_type", ""))
        dbps.length.set(params.get("length", "0"))
        dbps.default_val.set(params.get("default_val", ""))
        dbps.is_index.set(params.get("is_index", 0))
        dbps.view_col_type.set(params.get("view_col_type", "")) # Get From Property (setViewDataProperties)

        # Step 1 : Set View Data and Column Data
        dbps.col_id.set(ordercol_id)
        col_order_rank = dbhlp.setRankByColID(dbps) # Fetch Rank 
        if orderflag.upper() == "LEFT":
            order_rank = col_order_rank - 1
        else:
            order_rank = col_order_rank + 1
        getViewDataByID(viewps) # Get View Data
        viewhlp.setViewDataProperties(viewps) # Set View Properties
        dbps.table_id.set(viewps.table_id.get())
        dbps.table_name.set(viewps.table_name.get())
        dbhlp.getViewColumnCount(dbps)
        if dbps.tbl_col_cnt.get() not in (None, "", 0):
            dbps.col_cnt.set(dbps.tbl_col_cnt.get() + 1)

        # Step 2 : Add To Table Col
        colopt = {}
        tmpcnt = dbps.col_cnt.get()
        print("tmpcnt --> ", tmpcnt)
        match dbps.view_col_type.get():
            case "Status":
                colopt = dbhlp.getStatusColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                if dbps.default_val.get() == "":
                    dbps.default_val.set(0)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "DDL":
                colopt = dbhlp.getDropdownColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "YesNo":
                colopt = dbhlp.getYesNoColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                if dbps.default_val.get() == "":
                    dbps.default_val.set(0)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "TrueFalse":
                colopt = dbhlp.getTrueFalseColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                if dbps.default_val.get() == "":
                    dbps.default_val.set(0)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "People/Assign To":
                colopt = dbhlp.getPeopleColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, notify_user, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "Calc":
                colopt = dbhlp.getCalculationColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "Rating":
                colopt = dbhlp.getRatingColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                if dbps.default_val.get() == "":
                    dbps.default_val.set(0)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "Barcode":
                colopt = dbhlp.getBarcodeColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "Sign":
                colopt = dbhlp.getSignatureColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "Geolocation":
                colopt = dbhlp.getGeolocationColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                if dbps.default_val.get() == "":
                    dbps.default_val.set(0)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "Numbers":
                colopt = dbhlp.getNumberColParam(dbps.table_id.get(), dbps.col_alias.get(), order_rank)
                if dbps.is_index.get() == "":
                    dbps.is_index.set(0)
                if dbps.length.get() == "":
                    dbps.length.set(0)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "data_type", updval = dbps.data_type.get())
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "is_index", updval = dbps.is_index.get())
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "length", updval = dbps.length.get())
            case "Text":
                colopt = dbhlp.getTextColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "URL":
                colopt = dbhlp.getTextColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "Email":
                colopt = dbhlp.getTextColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "Tel":
                colopt = dbhlp.getTextColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "Colour":
                colopt = dbhlp.getTextColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "Upload":
                colopt = dbhlp.getTextColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "Date":
                colopt = dbhlp.getDateColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
            case "LastUpdated":
                colopt = dbhlp.getDateColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, order_rank)
                updateNestedJsonVal(fulljson = colopt, jsonkey = "col_options", srchkey= None, srchval = None, updkey = "default_val", updval = dbps.default_val.get())
        print("colopt --> ", colopt)
        col_name = colopt.get("col_name", "")
        dbps.col_id.set(0) 
        dbps.col_name.set(col_name)
        dbps.col_alias.set(colopt.get("col_alias", ""))
        col_options = colopt.get("col_options", {})
        dbps.col_options.set(col_options)
        dbps.rank.set(colopt.get("rank", 0))
        # insertUpdateTblCol(dbps) # Save to sys_new_db_tables_cols
        # updateDBTableSequence(dbps) # Update Sequence for DB Table
        # Update Col ID : Used in View Col
        updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= "col_name", srchval = col_name, updkey = "col_id", updval = dbps.col_id.get())
        view_cols = colopt.get("view_cols", {})
        print("view_cols --> ", view_cols)

        # Step 3 : Generate DB Query to Add Column
        dbps.alter_action.set("add_col")
        dbps.data_type.set(col_options.get("data_type", ""))
        dbps.length.set(col_options.get("length", 0))
        dbps.default_val.set(col_options.get("default_val", ""))
        generateDBColumnAlterQuery(dbps)
        print("alter_qry --> ", dbps.alter_qry.get())
        # DB.executStatementOnly(text(dbps.alter_qry.get()))
        return

        # Step 4 : Add New Column To View and update view Query
        view_json = viewps.view_cols.get()
        view_json["view_cols"].append(view_cols)
        sortObjectsByKey(view_json["view_cols"], 'rank', 'asc'); # Sort By Rank
        for i, col in enumerate(view_json["view_cols"]):
            col["rank"] = (i + 1) * 10
        viewps.view_name.set("")
        viewps.view_url.set("")
        viewps.view_type.set("")
        viewps.view_options.set("")
        viewps.view_cols.set(view_json)
        viewps.view_joins.set("")
        viewps.view_child.set("")
        viewps.view_actions.set("")
        viewps.dync_cat_id.set("")
        viewps.short_desc.set("")
        viewps.preview_img.set("")
        viewps.is_delete.set("")
        insertUpdateView(viewps)
        status = True
        message = dbps.col_alias.get() + " Added Successfully"
    except Exception as e:
        message = "Error in Adding Column"
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)
    # Output
    return JSONResponse (
        status_code = 200,
        content = {
            "status": status,
            "message": message,
            "new_col_id": dbps.col_id.get()
        }
    )

# http://testws1.localhost:8000/api/v1/dbtable/renamecol
def updateDBTblColAlias (request: Request):
    try:
        print("updateDBTblColAlias --> ")
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# http://testws1.localhost:8000/api/v1/dbtable/updatecol
def updateDBTableColumn (request: Request):
    print("updateDBTableColumn --> ")

# http://testws1.localhost:8000/api/v1/dbtable/removecol
def removeDBTableColumn (request: Request):
    print("removeDBTableColumn --> ")

# http://testws1.localhost:8000/api/v1/dbtable/getdesc
def getDBTableDesc (request: Request):
    print("getDBTableDesc --> ")