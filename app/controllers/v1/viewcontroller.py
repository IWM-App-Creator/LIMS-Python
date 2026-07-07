from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, globalps
import json
from app.properties.viewproperties import viewps
from app.properties.dbproperties import dbps
from app.dbfunctions.dbtablesfunctions import getDBTableData
from app.dbfunctions.viewfunctions import getViewDataByID
from app.dbfunctions.viewlayoutfunctions import getViewLayoutDataByID
from app.functions.viewhelper import processViewInputParam, setViewDataProperties

# http://xytovet.localhost:8000/api/v1/view/getdata?view_id=178
def getViewData (request: Request):
    try:
        # --------------------------
        # Get Input Param Data
        # --------------------------
        params = RequestData.params(request)
        processViewInputParam(viewps, params)
        # --------------------------
        # Get View Data
        # --------------------------
        userview = getViewDataByID(viewps) # Execute Function to User Get Data
        if not userview: # Invalid View
            raiseAPIError("View Not Found", 401)
        # for row in userview:
            # print(dict(row._mapping))

        viewps.userview.set(userview)
        setViewDataProperties(viewps) # Set View Properties
        # Get View Columns
        view_cols = viewps.view_cols.get()
        view_cols = view_cols.get("view_cols", [])
        col_id_arr = []
        for col in view_cols:
            col_id_arr.append(col["col_id"])
        col_id_arr = list(dict.fromkeys(col_id_arr))
        # Get Table Col
        dbps.col_ids.set(col_id_arr)
        dbps.is_del_tbl.set(0)
        dbps.is_del_col.set(0)
        tblcol = getDBTableData(dbps)
        tbl_cols = []
        for col in tblcol:
            col_options = (col.col_options or {}).copy()
            col_options.pop("csv_col_name", None)
            col_options.pop("csv_col_type", None)
            col_options.pop("csv_map_col_nm", None)
            tbl_cols.append({
                "col_id": col.col_id,
                "col_options": col_options
            })
        viewps.tbl_cols.set(tbl_cols)
        # Get View Layout Data
        viewlayout = getViewLayoutDataByID(viewps)
        if viewlayout:
            viewps.col_metadata.set(viewlayout.col_metadata)
            viewps.col_colors.set(viewlayout.col_colors)
            viewps.action_group_list.set(viewlayout.action_group_list)
            viewps.user_setting.set(viewlayout.user_setting)
        # --------------------------
        # Process To Get View Data
        # --------------------------
    except Exception as e:
        raiseAPIError(str(e), 500)

    # print("getViewData --> ", viewdata)

# http://xytovet.localhost:8000/api/v1/view/savetbldata
def saveTableData (request: Request):
    print("saveTableData --> ")

# http://xytovet.localhost:8000/api/v1/view/create
def createBlankView (request: Request):
    print("createBlankView --> ")

# http://xytovet.localhost:8000/api/v1/view/getlist
def getViewList (request: Request):
    print("getViewList --> ")

# http://xytovet.localhost:8000/api/v1/view/childstatus
def getViewChildStatus (request: Request):
    print("getViewChildStatus --> ")


# http://xytovet.localhost:8000/api/v1/view/duplicate
def duplicateFullView (request: Request):
    print("duplicateFullView --> ")

# http://xytovet.localhost:8000/api/v1/view/duplicateitem
def duplicateItemData (request: Request):
    print("duplicateItemData --> ")

# http://xytovet.localhost:8000/api/v1/view/lookupdata
def getLookupData (request: Request):
    print("getLookupData --> ")

# http://xytovet.localhost:8000/api/v1/view/filterdata
def getDataForFilter (request: Request):
    print("getDataForFilter --> ")


# http://xytovet.localhost:8000/api/v1/view/getquery
def getRawViewQuery (request: Request):
    print("getRawViewQuery --> ")

# http://xytovet.localhost:8000/api/v1/view/checkurl
def getViewURL (request: Request):
    print("getViewURL --> ")




    