from app.utils.common import Request, JSONResponse, RequestData, raiseAPIError
from app.dbfunctions.dbtablesfunctions import getDBTableData
from app.dbfunctions.dbfunctions import getTableColumnCount
from app.properties.dbproperties import dbps
from app.properties.viewproperties import viewps

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

# http://testws1.localhost:8000/api/v1/dbtable/addcol
def addDynamicColumn (request: Request):
    params = RequestData.params(request)

    view_col_type = params.get("view_col_type", "")
    dbps.view_col_type.set(view_col_type)
    # $view_id = empty(Input::get('view_id')) ? "0" : Input::get('view_id');
    # $col_alias = empty(Input::get('col_alias')) ? "" : Input::get('col_alias');
    # $view_col_type = empty(Input::get('view_col_type')) ? "" : Input::get('view_col_type');
    # $col_type = empty(Input::get('col_type')) ? "" : Input::get('col_type');
    # $txtcol_length = empty(Input::get('txtcol_length')) ? "1" : Input::get('txtcol_length');
    # $txtcol_dval = empty(Input::get('txtcol_dval')) ? "" : Input::get('txtcol_dval');
    # $txtcol_index = empty(Input::get('txtcol_index')) ? "0" : Input::get('txtcol_index');
    # $ordercol_id = empty(Input::get('ordercol_id')) ? "0" : Input::get('ordercol_id');
    # $orderflag = empty(Input::get('orderflag')) ? "Right" : Input::get('orderflag'); //Left - Right
    # $tab_id = empty(Input::get('tab_id')) ? "1" : Input::get('tab_id');
    # $all_usr_flg = empty(Input::get('all_usr_flg')) ? "0" : Input::get('all_usr_flg');
    # $notify_user = empty(Input::get('notify_user')) ? "0" : Input::get('notify_user');
    # $col_data_items = empty(Input::get('col_data_items')) ? "" : Input::get('col_data_items');
    # dbps.col_alias.set(params.get("view_id", ""))
    print("addDynamicColumn --> ")
    dbps.table_id.set(204)
    dbps.table_name.set("wtyrqqgmka")

    # Step 1 : Update Column Name For Specific Column Type
    if view_col_type in ("Status", "DDL", "YesNo", "TrueFalse", "People/Assign To", "Calc", "Rating", "Barcode", "Sign", "Geolocation") :
        match dbps.view_col_type.get():
            case "Status":
                dbps.tbl_col_srch.set("status_")
                col_name = "status_"
            case "DDL":
                dbps.tbl_col_srch.set("dd_")
                col_name = "dd_"
            case "YesNo":
                dbps.tbl_col_srch.set("yn_")
                col_name = "yn_"
            case "TrueFalse":
                dbps.tbl_col_srch.set("tf_")
                col_name = "tf_"
            case "People/Assign To":
                dbps.tbl_col_srch.set("ppl_")
                col_name = "ppl_"
            case "Calc":
                dbps.tbl_col_srch.set("calc_")
                col_name = "calc_"
            case "Rating":
                dbps.tbl_col_srch.set("rating_")
                col_name = "rating_"
            case "Barcode":
                dbps.tbl_col_srch.set("barcode_")
                col_name = "barcode_"
            case "Sign":
                dbps.tbl_col_srch.set("sign_")
                col_name = "sign_"
            case "Geolocation":
                dbps.tbl_col_srch.set("lat_")
                col_name = "lat_"
        getTableColumnCount(dbps)
        tmpcnt = dbps.tbl_col_cnt.get() + 1
        col_name = col_name + tmpcnt # Append Count + 1
        print(col_name)
    
    # Step 2 : Create Array For Adding New Column

    # Step 3 : Get Query For Adding Table Column

    # Step 4 : Add New Column To View

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