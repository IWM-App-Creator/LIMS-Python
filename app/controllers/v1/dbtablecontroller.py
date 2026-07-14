from app.utils.common import Request, JSONResponse, RequestData, raiseAPIError
from app.dbfunctions.dbtablesfunctions import getDBTableData, insertTableDataToDB, insertUpdateTblCol
from app.helper.dbhelper import setQueryColStmt, executeCreateTableQuery
from app.dbfunctions.viewfunctions import getViewDataByID
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

# http://testws1.localhost:8000/api/v1/dbtable/addcol?view_id=181&all_usr_flg=1&view_col_type=Status&col_alias=Status 2&default_val=&orderflag=Right&ordercol_id=3272&notify_user=0

def addDynamicColumn(request: Request):
    print("addDynamicColumn --> ")
    params = RequestData.params(request)
    viewps.view_id.set(params.get("view_id", 0))
    dbps.col_alias.set(params.get("col_alias", ""))
    col_name = params.get("col_alias", "").lower().replace(" ", "_")
    orderflag = params.get("orderflag", "Right")
    ordercol_id = params.get("ordercol_id", 0)
    notify_user = params.get("notify_user", 0)
    dbps.default_val.set(params.get("default_val", ""))
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
    dbps.col_cnt.set(dbps.tbl_col_cnt.get() + 1)

    # Step 2 : Add To Table Col
    colopt = {}
    tmpcnt = dbps.col_cnt.get()
    match dbps.view_col_type.get():
        case "Status":
            colopt = dbhlp.getStatusColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, dbps.default_val.get(), order_rank)
        case "DDL":
            colopt = dbhlp.getDropdownColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, dbps.default_val.get(), order_rank)
        case "YesNo":
            colopt = dbhlp.getYesNoColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, dbps.default_val.get(), order_rank)
        case "TrueFalse":
            colopt = dbhlp.getTrueFalseColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, dbps.default_val.get(), order_rank)
        case "People/Assign To":
            colopt = dbhlp.getPeopleColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, notify_user, dbps.default_val.get(), order_rank)
        case "Calc":
            colopt = dbhlp.getDropdownColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, dbps.default_val.get(), order_rank)
        case "Rating":
            colopt = dbhlp.getDropdownColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, dbps.default_val.get(), order_rank)
        case "Barcode":
            colopt = dbhlp.getDropdownColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, dbps.default_val.get(), order_rank)
        case "Sign":
            colopt = dbhlp.getDropdownColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, dbps.default_val.get(), order_rank)
        case "Geolocation":
            colopt = dbhlp.getDropdownColParam(dbps.table_id.get(), dbps.col_alias.get(), tmpcnt, dbps.default_val.get(), order_rank)
    col_name = colopt.get("col_name", "")
    dbps.col_id.set(0) 
    dbps.col_name.set(col_name)
    dbps.col_alias.set(colopt.get("col_alias", ""))
    col_options = colopt.get("col_options", {})
    dbps.col_options.set(col_options)
    dbps.rank.set(col_options.get("rank", 0))
    # insertUpdateTblCol(dbps) # Save to sys_new_db_tables_cols
    # dbhlp.updateDBTableSequence(dbps) # Update Sequence for DB Table
    # Update Col ID : Used in View Col
    updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= "col_name", srchval = col_name, updkey = "col_id", updval = dbps.col_id.get())
    view_cols = colopt.get("view_cols", {})

    # Step 3 : Generate DB Query to Add Column
    dbps.alter_action.set("add_col")
    dbps.data_type.set(col_options.get("data_type", ""))
    dbps.length.set(col_options.get("length", 0))
    dbps.default_val.set(col_options.get("default_val", ""))
    generateDBColumnAlterQuery(dbps)
    print(dbps.alter_qry.get())

    # Step 4 : Add New Column To View and update view Query
    view_json = viewps.view_cols.get()
    view_json["view_cols"].append(view_cols)
    sortObjectsByKey(view_json["view_cols"], 'rank', 'asc'); # Sort By Rank
    for i, col in enumerate(view_json["view_cols"]):
        col["rank"] = (i + 1) * 10
    print("view_json --> ", view_json)

    # Step 5 : Update Layout As Required

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