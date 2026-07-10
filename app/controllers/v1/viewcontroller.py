from app.utils.common import DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, nowWithTimeZone
from app.dbfunctions.viewfunctions import getViewDataByID, insertUpdateView
from app.dbfunctions.dbfunctions import getCreateTableSqlFromSchema
from app.dbfunctions.dbtablesfunctions import insertTableDataToDB, insertUpdateTblCol
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.functions.viewhelper import viewhlp, createviewhlp
from app.functions.dbhelper import setQueryColStmt, executeCreateTableQuery
from app.functions.generalfunctions import sortObjectsByKey, generateRandomString, addUpdateJson, updateNestedJsonVal, insertNestedJsonAfter, insertNestedJsonBefore, removeNestedJsonVal
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
        dbps.primary_col_nm.set(view_name.lower().replace(" ", "_") + "_id") 
        dbps.primary_col_alias.set(view_name + " ID")
        table_id = 0
        table_name = generateRandomString()
        v_c_item = []

        # Step 1 : Insert Into Sys DB Table
        # dbps.table_alias.set(view_name)
        # dbps.table_name.set(table_name)
        # table_id = insertTableDataToDB(dbps)
        # if not table_id:
        #     return raiseInvalidError("Table Not Created ", 401)
        # dbps.table_id.set(table_id)
        
        dbps.table_id.set(181)
        dbps.table_name.set("wtyrqqgmka")

        # Step 2 : Insert Into Sys DB Table Col
        createviewhlp.getDefaultAddViewCols(viewps) # Get Column List Based On View Type
        blank_view_cols = viewps.blank_view_cols.get()
        # dbps.colsql.set([]) # For SQL Query
        # dbps.colindex.set([]) # For SQL Query
        for blnkvcol in blank_view_cols:
            col_name = blnkvcol.get("col_name")
            dbps.col_id.set(0) 
            dbps.col_name.set(col_name)
            dbps.col_alias.set(blnkvcol.get("col_alias"))
            col_options = blnkvcol.get("col_options")
            dbps.col_options.set(col_options)
            dbps.rank.set(blnkvcol.get("rank"))
            # insertUpdateTblCol(dbps) # Save to sys_new_db_tables_cols
            # setQueryColStmt(dbps) # Set Col/Index For SQL Query
            # Set View Col Option To JSON
            if col_options.get("is_primary") == 1: # Set Primary Col ID & Name
                viewps.primary_col.set(f"{dbps.col_id.get()}")
                viewps.primary_colnm.set(col_name)
            if col_name == "is_delete": # Set Is Delete Col ID & Name
                viewps.delete_col.set(f"{dbps.col_id.get()}|is_delete")
            updateNestedJsonVal(fulljson = blnkvcol, jsonkey = "view_cols", srchkey= "col_name", srchval = col_name, updkey = "col_id", updval = dbps.col_id.get())
            view_cols = blnkvcol.get("view_cols")
            v_c_item.append(view_cols)
            

        # Step 3 : Generate Create Table Query & Execute
        # executeCreateTableQuery(dbps)

        # Step 4 : Insert Into Sys View Table
        # viewps.table_id.set(table_id)
        # # viewps.table_name.set(table_name)
        viewps.table_id.set(181)
        viewps.table_name.set("wtyrqqgmka")
        view_cols = {}
        view_cols["view_cols"] = v_c_item
        viewps.view_cols.set(view_cols)
        # print("v_c_item --> ", viewps.view_cols.get())
        
        createviewhlp.getDefaultViewOptions(viewps) # Get View Options

        # Generate Query 
        createviewhlp.generateViewQuery(viewps)
        createviewhlp.getLeftJoinQuery(viewps)
        createviewhlp.getFullViewQuery(viewps)
        
        # TO DO
        # Append Query To View Options
        # $dvps->view_options = $GeneralFunctions->addUpdateToJson($gfps, "view_qry", $dvps->db_query, $dvps->view_options); 

        # viewps.view_joins.set({"view_joins": []})
        # viewps.view_child.set({"view_child": []})
        # viewps.view_actions.set({"view_actions": []})
        # insertUpdateView(viewps)

        # Step 5 : Set Menu
        # insertUpdateView(viewps)

        # $viewdtl = explode("~~", $viewdtl);
        # $view_id = $viewdtl[0];
        # $view_url = "https://" . $GeneralFunctions->getDomainNameFromURL() . "/view/" . $viewdtl[2];
        # if($pin_to_menu == 1) {
        #     $ModelFunctionsController->addViewToMenu($user_id, $view_id, $view_name);
        # }
        
        # /* Step 4 : Update Rank */

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
