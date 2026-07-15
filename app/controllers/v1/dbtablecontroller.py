from app.utils.common import Request, JSONResponse, RequestData, raiseAPIError, DB, text, raiseInvalidError
from app.dbfunctions.dbtablesfunctions import getDBTableData, insertTableDataToDB, insertUpdateTblCol, updateDBTableSequence
from app.helper.dbhelper import setQueryColStmt, executeCreateTableQuery
from app.dbfunctions.viewfunctions import getViewDataByID, insertUpdateView, updateViewCols
from app.dbfunctions.dbfunctions import generateDBColumnAlterQuery
from app.helper.viewhelper import viewhlp, createviewhlp
from app.helper import dbhelper as dbhlp
from app.properties.dbproperties import dbps
from app.properties.viewproperties import viewps
from app.helper.generalfunctions import sortObjectsByKey, updateNestedJsonVal
from app.helper.dbaddcolhelper import getColumnParams

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
def getDBTableColumns(request: Request):
    print("getDBTableColumns --> ")
    try:
        params = RequestData.params(request)
        dbps.table_id.set(params.get("table_id", 0))
        if dbps.table_id.get() in (None, "", 0):
            return raiseInvalidError("Table ID Not Found", 401)
        table_data = getDBTableData(dbps) # Get DB Table Data
        db_tbl = []
        for tbl in table_data:
            if tbl.col_name not in ("is_delete", "is_metadata"):
                row = {
                    "table_id": tbl.table_id,
                    "table_name": tbl.table_name,
                    "table_alias": tbl.table_alias,
                    "col_id": tbl.col_id,
                    "col_name": tbl.col_name,
                    "col_alias": tbl.col_alias,
                    "col_options": tbl.col_options
                }
                db_tbl.append(row)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "DB Table Data",
                "db_tbl": db_tbl
            }
        )
    except Exception as e:
        # saveErrorLogtoDB ("DBTable", dbps.table_id.get(), "getDBTableColumns", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)
    

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
        orderflag = params.get("orderflag", "Right")
        ordercol_id = params.get("ordercol_id", 0)
        viewps.view_id.set(params.get("view_id", 0))
        dbhlp.setDBParams(dbps, params)

        # Step 1 : Set View Data and Order Rank or Column
        dbps.col_id.set(ordercol_id)
        col_order_rank = dbhlp.setRankByColID(dbps) # Fetch Rank 
        if orderflag.upper() == "LEFT":
            order_rank = col_order_rank - 1
        else:
            order_rank = col_order_rank + 1
        dbps.rank.set(order_rank)
        getViewDataByID(viewps) # Get View Data
        viewhlp.setViewDataProperties(viewps) # Set View Properties
        # Set Table To DB Properties
        dbps.table_id.set(viewps.table_id.get())
        dbps.table_name.set(viewps.table_name.get())
        dbhlp.getViewColumnCount(dbps)
        if dbps.tbl_col_cnt.get() not in (None, ""):
            dbps.col_cnt.set(dbps.tbl_col_cnt.get() + 1)

        # Step 2 : Add To Table Col
        colopt = getColumnParams(dbps)
        dbps.col_id.set(0) 
        dbps.col_name.set(colopt.get("col_name", ""))
        dbps.col_alias.set(colopt.get("col_alias", ""))
        col_options = colopt.get("col_options", {})
        dbps.col_options.set(col_options)
        dbps.rank.set(colopt.get("rank", 0))
        insertUpdateTblCol(dbps) # Save to sys_new_db_tables_cols
        updateDBTableSequence(dbps) # Update Sequence for DB Table
        # Update Col ID : Used in View Col
        updateNestedJsonVal(fulljson = colopt, jsonkey = "view_cols", srchkey= "col_name", srchval = dbps.col_name.get(), updkey = "col_id", updval = dbps.col_id.get())
        view_cols = colopt.get("view_cols", {})

        # Step 3 : Generate DB Query to Add Column
        dbps.alter_action.set("add_col")
        dbps.data_type.set(col_options.get("data_type", ""))
        dbps.length.set(col_options.get("length", 0))
        dbps.default_val.set(col_options.get("default_val", ""))
        generateDBColumnAlterQuery(dbps)
        DB.executStatementOnly(text(dbps.alter_qry.get()))

        # Step 4 : Add New Column To View and update view Query
        view_json = viewps.view_cols.get()
        view_json["view_cols"].append(view_cols)
        sortObjectsByKey(view_json["view_cols"], 'rank', 'asc'); # Sort By Rank
        for i, col in enumerate(view_json["view_cols"]):
            col["rank"] = (i + 1) * 10
        viewps.view_cols.set(view_json)
        createviewhlp.generateViewQuery(viewps)
        createviewhlp.getLeftJoinQuery(viewps)
        createviewhlp.getFullViewQuery(viewps)
        createviewhlp.getDefaultViewOptions(viewps) # Set View Options
        viewps.view_name.set("")
        viewps.view_url.set("")
        viewps.view_type.set("")
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
        # saveErrorLogtoDB ("DBTable", viewps.view_id.get(), "addDynamicColumn", str(e)) # Log Error To DB
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
def updateDBTblColAlias(request: Request):
    try:
        print("updateDBTblColAlias --> ")
        params = RequestData.params(request)
        dbps.col_id.set(params.get("col_id", 0))
        dbps.col_alias.set(params.get("col_alias", ""))
        viewps.view_id.set(params.get("view_id", 0))
        flag = params.get("flag", "")
        if dbps.col_id.get() in (None, "", 0):
            return raiseInvalidError("Column ID Not Found", 401)
        if flag.upper() == "COL":
            insertUpdateTblCol(dbps)
        elif flag.upper() == "VIEW":
            getViewDataByID(viewps) # Get View Data
            viewhlp.setViewDataProperties(viewps) # Set View Properties
            updateNestedJsonVal(fulljson = viewps.view_cols.get(), jsonkey = "view_cols", srchkey= "col_id", srchval = dbps.col_id.get(), updkey = "col_alias", updval = dbps.col_alias.get())
            updateViewCols(viewps) # Save to Dynamic View
            # Update in View Layout
        elif flag.upper() == "USER":
            print("User Update")
            # Update in View Layout
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