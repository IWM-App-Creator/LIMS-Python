from app.utils.common import Request, JSONResponse, RequestData, raiseAPIError
from app.dbfunctions.dbtablesfunctions import getDBTableData
from app.dbfunctions.dbfunctions import getTableColumnCount
from app.dbfunctions.viewfunctions import getViewDataByID
from app.helper.viewhelper import viewhlp
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
# miidata/api/dyncol/add?user_id=3779&api_secret=w@lHB)6*2AVsZf.spyff&view_id=181&col_id=0&tab_id=0&all_usr_flg=1&col_type=Status&col_name=status_2&col_alias=Status 2&txt_data_type=int&txtcol_length=4&txtcol_index=1&txtcol_dval=0&is_private=0&dync_cat_id=0&orderflag=Right&ordercol_id=3272&notify_user=0

def addDynamicColumn (request: Request):
    params = RequestData.params(request)

    print("addViewColumn --> ")
    params = RequestData.params(request)
    viewps.view_id.set(params.get("view_id", "0"))
    
    col_alias = params.get("col_alias", "0")
    col_name = col_alias.lower().replace(" ", "_")
    
    viewps.col_alias.set(col_alias)
    # viewps.col_name.set(col_name)

    # col_type -->  STATUS
    # =Status
    # &
    # &=Status 2
    # &txt_data_type=int&txtcol_length=4&txtcol_index=1&txtcol_dval=0
    # &is_private=0
    # &dync_cat_id=0
    # &orderflag=Right
    # &ordercol_id=3272
    # &notify_user=0
    
    # view_cols": {"col_id": "", "col_name": col_name, "col_alias": col_alias, "col_type": "NUMBER", "qry_alias": "mtbl", "col_key": 1, "link_text": "", "url_prefix": "", "date_format": "", "calc_formula": "", "lookup_colid": 0, "lookup_colnm": "", "rank": rank} }

    # Step 1 : Get View Data
    getViewDataByID(viewps) # Get View Data
    viewhlp.setViewDataProperties(viewps) # Set View Properties

    view_col_type = params.get("view_col_type", "") # Get From Property (setViewDataProperties)
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
    print("col_name --> ", col_name)
        
    # Step 2 : Add To Table Col 
        # getStatusColParam
        # col_options --> viewcols mate
        # view_cols --> for View
        
        # Log --> Don't save

    # Step 3 : Generate DB Add Column Query
        # Log --> Don't save

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