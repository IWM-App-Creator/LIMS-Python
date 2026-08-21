import json
from app.utils.common import DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, nowWithTimeZone, userps
from app.dbfunctions.viewfunctions import getViewDataByID, insertUpdateView
from app.dbfunctions.dbfunctions import getCreateTableSqlFromSchema
from app.dbfunctions.dbtablesfunctions import insertTableDataToDB, insertUpdateTblCol
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.filterfunctions import getFilterData
from app.dbfunctions.menufunctions import getActiveMenuDB, insertUpdateMenuCentre
from app.helper.viewhelper import viewhlp, createviewhlp
from app.helper.dbhelper import setQueryColStmt, executeCreateTableQuery
from app.helper.generalfunctions import sortObjectsByKey, generateRandomString, addUpdateJson, updateNestedJsonVal, insertNestedJsonAfter, insertNestedJsonBefore, removeNestedJsonVal, getHostName
from app.properties.viewproperties import viewps
from app.properties.dbproperties import dbps
from app.properties.menuproperties import menups
from app.properties.dashboardproperties import dps
from app.properties.widgetproperties import widgetps

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
        if viewps.output_type.get() != "viewdata":
            viewhlp.setViewTableCols(viewps) # Get View Columns
        viewhlp.setViewLayout(viewps) # Get View Layout Data
        # --------------------------
        # Sort View Col
        # --------------------------
        view_cols = viewps.view_cols.get()
        sortObjectsByKey(view_cols, 'rank', 'asc'); # Sort By Rank
        viewps.view_cols.set(view_cols)
        # --------------------------
        # Get Data
        # --------------------------
        dataarr = []
        viewps.view_qry_data.set(dataarr)
        view_qry = viewps.view_qry.get() # Get Query
        # check Main Table Delete Records
        if viewps.show_deleted.get() in (0, "0", None):
            view_qry = view_qry + " AND mtbl.is_delete = 0"
        # set Filter Qry by calling from Dashboard
        if viewps.call_from.get() == "Dashboard":
            dps.dashboard_id.set(params.get("dashboard_id"))
            widgetps.widget_ref_id.set(params.get("widget_ref_id"))
            viewhlp.setDashboardFilterQry(viewps, dps, widgetps)
        # Set Group By Data
        groupcndt = viewhlp.setViewGroupByData(viewps)
        if groupcndt not in (None, ""):
            view_qry = view_qry + " AND (" + groupcndt + ")"
        # get Filter from Save Result Table
        if viewps.filter_qry.get() in (None, ""):
            viewhlp.checkDefaultFilter(viewps)
        # Set Search Query
        if viewps.search_text.get() not in (None, ""):
            view_qry = view_qry + " AND (" + viewhlp.getViewSearchQuery(viewps) + ")"
        # Set Filter Query
        if viewps.filter_qry.get() not in (None, ""):
            view_qry = view_qry + " AND (" + viewps.filter_qry.get() + ")"
        # Check Association
        if userps.ws_role_id.get() != 1 and userps.role_id.get() != 1:
            viewhlp.checkViewAssociation(viewps) # Check Associations
            if viewps.association_qry.get():
                view_qry = view_qry + " AND (" + viewps.association_qry.get() + ")"
        # Set Association Status Limit
        stslmtqry = viewhlp.setAssociationStatusLimit(viewps)
        if stslmtqry not in (None, ""):
            view_qry = view_qry + " AND (" + stslmtqry + ")"
        # Set Child View Condition
        if viewps.is_child.get() not in (None, "", 0, "0") and viewps.api_param.get() not in (None, "", 0, "0"):
            view_qry = view_qry + " AND (" + viewps.api_param.get() + " = " + str(viewps.api_param_val.get() or "") + ")"
        # Set View Data Sorting
        viewhlp.setViewSorting(viewps)
        view_qry = f"{view_qry} Order By {viewps.sorting.get()}"
        viewhlp.setViewPaging(viewps) # Get Paging
        view_qry = view_qry.replace("#USER_ID#", str(userps.user_id.get())) # Update Notification Query User ID
        view_qry = f"{view_qry} LIMIT {viewps.offset.get()}, {viewps.page_size.get()}"
        viewps.view_qry.set(view_qry)
        # print(view_qry)
        # return
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
        print("getViewData Exception SubDomain --> ", userps.req_subdomain.get())
        saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        # raiseAPIError(str(e), 500)
        return JSONResponse (
            status_code = 500,
            content = {
                "status": False,
                "message": "View Error",
                "user_id": userps.user_id.get(),
                "ws_role_id": userps.ws_role_id.get(),
                "workspace_id": userps.workspace_id.get(),
                "schema_name": userps.schema_name.get(),
                "req_host": userps.req_host.get(),
                "req_subdomain": userps.req_subdomain.get(),
                "error" : str(e)
            }
        )

# http://xytovet.localhost:8000/api/v1/view/savetbldata
# api/v1/view/savetbldata?view_id=183&item_id=8&table_name=mmydbptppt&col_name=status_1&primary_colnm=python___react_v2_id&col_val=924
def saveTableData(request: Request):
    try:
        params = RequestData.params(request)
        viewhlp.setViewInputParam(viewps, params) # Get Input Param Data
        viewhlp.generateTblUpdateQry(viewps) # Generate Update Query
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Table Data Updated Successfully"
            }
        )
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "saveTableData", str(e)) # Log Error To DB
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
        # Step 1 : Insert Into Sys DB Table
        dbps.table_alias.set(view_name)
        dbps.table_name.set(table_name)
        table_id = insertTableDataToDB(dbps)
        if not table_id:
            return raiseInvalidError("Table Not Created ", 401)
        dbps.table_id.set(table_id)

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
        viewps.view_cols.set(v_c_item)
        # Generate Query 
        createviewhlp.generateViewQuery(viewps)
        createviewhlp.getLeftJoinQuery(viewps)
        createviewhlp.getFullViewQuery(viewps)
        createviewhlp.getDefaultViewOptions(viewps) # Set View Options
        viewps.view_joins.set([]) # Set View Joins Tables
        viewps.view_child.set([]) # Set View Child
        viewps.view_actions.set([{"act_icon": "trash", "action_id": 3, "action_label": "Delete", "rank": 1, "is_dynamic": 0, "act_prm_ids": "", "act_bg_color": "", "input_params": "", "view_act_json": ""}, {"act_icon": "refresh-ccw", "action_id": 2, "action_label": "Restore", "rank": 2, "is_dynamic": 0, "act_prm_ids": "", "act_bg_color": "", "input_params": "", "view_act_json": ""}]) # Set View Actions
        insertUpdateView(viewps)

        # Step 5 : Set Menu If Pin
        if viewps.pin_to_menu.get() in (1, "1"):
            menu_data = getActiveMenuDB(menups)
            menu_json = getattr(menu_data, "menu_json", [])
            if isinstance(menu_json, str):
                menu_json = eval(menu_json)
            if not isinstance(menu_json, list):
                menu_json = []
            menu_json.append({"m_type": "view", "item_id": viewps.view_id.get(), "menu_id": 0, "subMenu": [], "menu_url": view_url, "menu_icon": "", "menu_name": view_name, "is_new_tab": 0, "is_section": 0, "menu_color": "", "parent_menu_id": 0})
            menups.upd_vals.set({"menu_json": menu_json})
            insertUpdateMenuCentre(menups)

        # Step 6 : Return JSON
        getHostName(request)
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

# http://xytovet.localhost:8000/api/v1/view/filterdata
def getDataForFilter(request: Request):
    print("getDataForFilter --> ")

# http://xytovet.localhost:8000/api/v1/view/getquery
def getRawViewQuery(request: Request):
    print("getRawViewQuery --> ")

# http://xytovet.localhost:8000/api/v1/view/checkurl
def getViewURL(request: Request):
    print("getViewURL --> ")
