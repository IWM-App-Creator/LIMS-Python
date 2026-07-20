from app.utils.common import DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, nowWithTimeZone, userps
from app.dbfunctions.viewfunctions import getViewDataByID, insertUpdateView
from app.dbfunctions.dbfunctions import getCreateTableSqlFromSchema
from app.dbfunctions.dbtablesfunctions import insertTableDataToDB, insertUpdateTblCol
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.helper.viewhelper import viewhlp, createviewhlp
from app.helper.dbhelper import setQueryColStmt, executeCreateTableQuery
from app.helper.generalfunctions import sortObjectsByKey, generateRandomString, addUpdateJson, updateNestedJsonVal, insertNestedJsonAfter, insertNestedJsonBefore, removeNestedJsonVal, getHostName
from app.properties.viewproperties import viewps
from app.properties.dbproperties import dbps
from app.properties.menuproperties import menups

# http://testws1.localhost:8000/api/v1/view/getdata?view_id=125
# http://testws1.localhost:8000/api/v1/view/getdata?view_id=178
# http://testws1.localhost:8000/api/v1/view/getdata?view_id=182
def getViewData(request: Request):
    try:
        params = RequestData.params(request)
        viewhlp.setViewInputParam(viewps, params) # Get Input Param Data
        getViewDataByID(viewps) # Get View Data
        if not viewps.userview.get(): # Invalid View
            return raiseInvalidError("View Not Found", 404)
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
        
        viewhlp.checkViewAssociation(viewps) # Check Associations
        # print("association_qry --", viewps.association_qry.get())
        if viewps.association_qry.get():
            view_qry = view_qry + " AND ( " + viewps.association_qry.get() + ")"
        
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
        #

        sorting = f"mtbl.{viewps.primary_colnm.get()} DESC"
        # viewps.sorting.set(sorting)
        # viewps.primary_colnm.set(0)
        # setViewSorting(viewps) # Get Sorting
        # print("primary_colnm --> ", viewps.primary_colnm.get())
        #     if($dvps->sorting) {
                # $dvps->view_qry = $dvps->view_qry . " order by " . $dvps->sorting;
        #     }
        view_qry = f"{view_qry} Order By {sorting}"
        viewhlp.setViewPaging(viewps) # Get Paging
        view_qry = view_qry.replace("#USER_ID#", str(userps.user_id.get())) # Update Notification Query User ID
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
    
        # Association View Wise
        # $tmpdata = array();
        # $tmpdata['view_id'] = $view_id;
        # $tmpdata['admin_access'] = $admin_access;
        # $tmpdata['association_access'] = $association_access;
        # $tmpdata['association_users'] = $association_users;
        # if($association_view) {
        #     $tmpdata['asso_view_id'] = $association_view->asso_view_id;
        #     $tmpdata['view_asso_json'] = json_decode($association_view->view_asso_json);
        # } else {
        #     $tmpdata['asso_view_id'] = "";
        #     $tmpdata['view_asso_json'] = [];
        # }
    except Exception as e:
        saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# http://xytovet.localhost:8000/api/v1/view/savetbldata
def saveTableData(request: Request):
    try:
        print("saveTableData --> ")
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# http://testws1.localhost:8000/api/v1/view/create?view_name=reactv1&view_type=Table&pin_to_menu=0&m_centre_id=1
def createBlankView(request: Request):
    try:
        params = RequestData.params(request)
        view_name = params.get("view_name", "")
        viewps.view_name.set(view_name)
        viewps.view_type.set(params.get("view_type", ""))
        viewps.pin_to_menu.set(params.get("pin_to_menu", 0))
        menups.m_centre_id.set(params.get("m_centre_id", 0))
        dbps.primary_col_nm.set(view_name.lower().replace(" ", "_") + "_id") 
        dbps.primary_col_alias.set(view_name + " ID")
        table_id = 0
        table_name = generateRandomString()
        v_c_item = []
        print("view_name --> ", view_name)
        print("table_name --> ", table_name)
        # Step 1 : Insert Into Sys DB Table
        dbps.table_alias.set(view_name)
        dbps.table_name.set(table_name)
        table_id = insertTableDataToDB(dbps)
        if not table_id:
            return raiseInvalidError("Table Not Created ", 401)
        dbps.table_id.set(table_id)
        print("table_id --> ", dbps.table_id.get())

        # Step 2 : Insert Into Sys DB Table Col
        createviewhlp.getDefaultAddViewCols(viewps) # Get Column List Based On View Type
        blank_view_cols = viewps.blank_view_cols.get()
        dbps.colsql.set([]) # For SQL Query
        dbps.colprimary.set("") # For SQL Query
        dbps.colindex.set([]) # For SQL Query

        # print("table_id --> ", dbps.table_id.get())
        for blnkvcol in blank_view_cols:
            col_name = blnkvcol.get("col_name")
            dbps.col_id.set(0) 
            dbps.col_name.set(col_name)
            dbps.col_alias.set(blnkvcol.get("col_alias"))
            col_options = blnkvcol.get("col_options")
            dbps.col_options.set(col_options)
            dbps.rank.set(blnkvcol.get("rank"))
            insertUpdateTblCol(dbps) # Save to sys_new_db_tables_cols
            setQueryColStmt(dbps) # Set Col/Index For SQL Query
            # Set View Col Option To JSON
            if col_options.get("is_primary") == 1: # Set Primary Col ID & Name For View Options
                viewps.primary_col.set(f"{dbps.col_id.get()}")
                viewps.primary_colnm.set(col_name)
            if col_name == "is_delete": # Set Is Delete Col ID & Name For View Options
                viewps.delete_col.set(f"{dbps.col_id.get()}|is_delete")

            if col_name not in ("is_delete", "is_metadata"): # Excluded Columns From View
                updateNestedJsonVal(fulljson = blnkvcol, jsonkey = "view_cols", srchkey= "col_name", srchval = col_name, updkey = "col_id", updval = dbps.col_id.get())
                view_cols = blnkvcol.get("view_cols")
                v_c_item.append(view_cols)

        # Step 3 : Generate Create Table Query & Execute
        executeCreateTableQuery(dbps)

        # Step 4 : Insert Into Sys View Table
        viewps.table_id.set(table_id)
        viewps.table_name.set(table_name)
        view_url = generateRandomString(length = 12, hasdigits = 1)
        viewps.view_url.set(view_url)
        view_cols = {}
        view_cols["view_cols"] = v_c_item
        viewps.view_cols.set(view_cols)
        # Generate Query 
        createviewhlp.generateViewQuery(viewps)
        createviewhlp.getLeftJoinQuery(viewps)
        createviewhlp.getFullViewQuery(viewps)
        createviewhlp.getDefaultViewOptions(viewps) # Set View Options
        viewps.view_joins.set({"view_joins": []}) # Set View Joins Tables
        viewps.view_child.set({"view_child": []}) # Set View Child
        viewps.view_actions.set({"view_actions": []}) # Set View Actions
        insertUpdateView(viewps)
        print("view_id --> ", viewps.view_id.get())

        # Step 5 : Set Menu If Pin
        # if viewps.pin_to_menu.get() == 1:
            # menups.menu_name.set(view_name)
            # menups.m_type.set(1)
            # menups.view_id.set(viewps.view_id.get())
            # getLastMenuRankByCMID(menups) # Get Last Menu Rank
            # insertUpdateUserMenu(menups) # Add To Menu

        # Step 6 : Return JSON
        getHostName(request)
        view_url = "https://" + userps.req_host.get() + "/view/" + view_url
        print("view_url --> ", view_url)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "View Created Successfully!",
                "view_id": viewps.view_id.get(),
                "view_url": view_url,
            }
        )
    except Exception as e:
        saveErrorLogtoDB ("CreateView", 0, "createBlankView", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# http://xytovet.localhost:8000/api/v1/view/getlist
def getViewList(request: Request):
    try:
        print("getViewList --> ")
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# http://xytovet.localhost:8000/api/v1/view/childstatus
def getViewChildStatus(request: Request):
    try:
        print("getViewChildStatus --> ")
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# http://xytovet.localhost:8000/api/v1/view/duplicate
def duplicateFullView(request: Request):
    print("duplicateFullView --> ")

# http://xytovet.localhost:8000/api/v1/view/duplicateitem
def duplicateItemData(request: Request):
    print("duplicateItemData --> ")

# http://xytovet.localhost:8000/api/v1/view/lookupdata
def getLookupData(request: Request):
    print("getLookupData --> ")
    params = RequestData.params(request)

# http://xytovet.localhost:8000/api/v1/view/filterdata
def getDataForFilter(request: Request):
    print("getDataForFilter --> ")

# http://xytovet.localhost:8000/api/v1/view/getquery
def getRawViewQuery(request: Request):
    print("getRawViewQuery --> ")

# http://xytovet.localhost:8000/api/v1/view/checkurl
def getViewURL(request: Request):
    print("getViewURL --> ")
