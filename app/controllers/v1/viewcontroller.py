from app.utils.common import DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, nowWithTimeZone
from app.dbfunctions.viewfunctions import getViewDataByID
from app.dbfunctions.dbtablesfunctions import insertTableDataToDB, insertUpdateTblCol
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.functions.viewhelper import viewhlp, createviewhlp
from app.functions.generalfunctions import sortObjectsByKey, generateRandomString
from app.properties.viewproperties import viewps
from app.properties.dbproperties import dbps

# http://testws1.localhost:8000/api/v1/view/getdata?view_id=178
def getViewData(request: Request):
    try:
        params = RequestData.params(request)
        viewhlp.setViewInputParam(viewps, params) # Get Input Param Data
        getViewDataByID(viewps) # Get View Data
        if not viewps.userview.get(): # Invalid View
            return raiseInvalidError("View Not Found", 401)
        viewhlp.setViewDataProperties(viewps) # Set View Properties
        viewhlp.setViewTableCols(viewps) # Get View Columns
        viewhlp.setViewLayout(viewps) # Get View Layout Data
        # --------------------------
        # Sort View Col
        # --------------------------
        view_cols = viewps.view_cols.get()
        sortObjectsByKey(view_cols["view_cols"], 'rank', 'asc'); # Sort By Rank
        viewps.view_cols.set(view_cols)
        # --------------------------
        # Get Data
        # --------------------------
        dataarr = []
        viewps.view_qry_data.set(dataarr)
        view_qry = viewps.view_qry.get() # Get Query
        # print("primary_colnm --", viewps.primary_colnm.get())
        #     $dvps->rawqry = "";
        #     if($dvps->txtsearch) {
        #         $this->getViewSearchQuery($dvps);
        #         // $DynamicViewFunctions->appendChildViewSearchQuery($dvps); /* Search For Child View */
        #         if($dvps->rawqry) {
        #             $dvps->view_qry = $dvps->view_qry . " and ( " . $dvps->rawqry . " ) ";
        #         }
        #     }
        #     if($dvps->filterqry) {
        #         $this->getViewFilteredQuery($dvps);
        #     }
        #     // if($dvps->association_limit) {
        #     //     $DynamicViewFunctions->getViewAssociationLimit($dvps);
        #     // }
        #     // checkViewAssociation.
        sorting = f"mtbl.{viewps.primary_colnm.get()} DESC"
        # viewps.sorting.set(sorting)
        # viewps.primary_colnm.set(0)
        # setViewSorting(viewps) # Get Sorting
        # print("primary_colnm --", viewps.primary_colnm.get())
        #     if($dvps->sorting) {
                # $dvps->view_qry = $dvps->view_qry . " order by " . $dvps->sorting;
        #     }
        view_qry = f"{view_qry} Order By {sorting}"
        viewhlp.setViewPaging(viewps) # Get Paging
        view_qry = f"{view_qry} LIMIT {viewps.offset.get()}, {viewps.page_size.get()}"
        viewps.view_qry.set(view_qry)
        view_qry_data = DB.executeDBStatement(view_qry) # Execute Query To Get View Data
        viewps.view_qry_data.set(view_qry_data)
        viewhlp.getRecordCount(viewps) # Total Record Data
        viewhlp.setViewItemArray(viewps); # Set View Data In Items Array
        viewhlp.setViewOutputArray(viewps); # Output Json
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "View Data",
                "view_data": viewps.output_array.get()
            }
        )
    except Exception as e:
        saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# http://xytovet.localhost:8000/api/v1/view/savetbldata
def saveTableData (request: Request):
    try:
        print("saveTableData --> ")
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# http://xytovet.localhost:8000/api/v1/view/create?view_name=Python View&view_type=Table&pin_to_menu=1

# api/dyncol/add?view_id=166&col_id=0&tab_id=0&all_usr_flg=1&col_type=DDL&col_alias=DDl&txt_data_type=varchar&txtcol_length=255&txtcol_index=0&txtcol_dval=&orderflag=Right&ordercol_id=3017&notify_user=0
def createBlankView (request: Request):
    try:
        params = RequestData.params(request)
        view_name = params.get("view_name", "")
        viewps.view_name.set(view_name)
        viewps.view_type.set(params.get("view_type", ""))
        viewps.pin_to_menu.set(params.get("pin_to_menu", 0))


        #
        dbps.table_id.set(204)
        dbps.table_name.set("wtyrqqgmka")


        # dbps.primary_col_nm.set(view_name.lower().replace(" ", "_") + "_id") 
        # dbps.primary_col_alias.set(view_name + " ID")
        # print("primary_col_nm --> ", dbps.primary_col_nm.get())
        # print("primary_col_alias --> ", dbps.primary_col_nm.get())

        # Step 1 Insert Into Sys DB Table
        # dbps.table_alias.set(view_name)
        # dbps.table_name.set(generateRandomString())
        # table_id = insertTableDataToDB(dbps)
        # if not table_id:
        #     return raiseInvalidError("Table Not Created ", 401)
        # dbps.table_name.set(table_id)
        # print("table_id --> ", table_id)
        # table_id = 204
        # table_name = "krxtqesaep"
        dbps.table_id.set(204)

        # Step 2 Insert Into Sys DB Table Col
        createviewhlp.getDefaultAddViewCols(viewps)

        blank_view_cols = viewps.blank_view_cols.get()
        for blnkvcol in blank_view_cols:
            # col_name = getattr(blnkvcol, "col_name", "")
            print("blnkvcol --> ", blnkvcol)
            print("blnkvcol --> ", blnkvcol.get("col_name", ""))
            # setColOptions(dbps)
            # insertUpdateTblCol(dbps)
            # setColForView(dbps)

        # print("blank_view_cols --> ", viewps.blank_view_cols.get())
        # Step 3 Insert Into Sys View Table


        # print("createBlankView  --> ", nowWithTimeZone())
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# http://xytovet.localhost:8000/api/v1/view/getlist
def getViewList (request: Request):
    try:
        print("getViewList --> ")
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# http://xytovet.localhost:8000/api/v1/view/childstatus
def getViewChildStatus (request: Request):
    try:
        print("getViewChildStatus --> ")
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

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
