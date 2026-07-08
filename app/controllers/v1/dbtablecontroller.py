from app.utils.common import Request, JSONResponse
from app.properties.dbproperties import dbps
from app.dbfunctions.dbtablesfunctions import getDBTableData

# http://xytovet.localhost:8000/api/v1/dbtable/gettbls
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

# http://xytovet.localhost:8000/api/v1/dbtable/getcols
def getDBTableColumns (request: Request):
    print("getDBTableList --> ")

# http://xytovet.localhost:8000/api/v1/dbtable/updatetbl
def updateDBTableAlias (request: Request):
    print("updateDBTableAlias --> ")

# http://xytovet.localhost:8000/api/v1/dbtable/renamecol
def updateDBTblColAlias (request: Request):
    print("updateDBTblColAlias --> ")

# http://xytovet.localhost:8000/api/v1/dbtable/updatecol
def updateDBTableColumn (request: Request):
    print("updateDBTableColumn --> ")

# http://xytovet.localhost:8000/api/v1/dbtable/removecol
def removeDBTableColumn (request: Request):
    print("removeDBTableColumn --> ")

# http://xytovet.localhost:8000/api/v1/dbtable/getdesc
def getDBTableDesc (request: Request):
    print("getDBTableDesc --> ")