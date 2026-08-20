from app.utils.common import JSONResponse, Request, RequestData, raiseAPIError, raiseInvalidError
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.helper.systemviewhelper import getSystemView
from app.properties.systemviewproperties import systemviewps

def getSystemViewList(request: Request):
    try:
        params = RequestData.params(request)
        view_name = params.get("view_name", "").lower()
        systemviewps.view_name.set(view_name)
        systemviewps.page_no.set(params.get("page_no", 1))
        systemviewps.filter_qry.set(params.get("filter_qry", ""))
        systemviewps.search_text.set(params.get("search_text", ""))

        # Create 1 Table & Save Meta Data For Colarray.
        systemviewps.table_name.set("lims_expense_master") # temporary default, if no mapping table found redirect to 404..
        colarray = ["expense_id-Expense ID", "expense_name-Expense Name", "rate-Rate", "created_date-Created Date"]
        if view_name == "labour": 
            systemviewps.table_name.set("lims_labour_master")
            colarray = ["labour_id-Labour ID", "labour_name-Labour Name", "hourly_rate-Hourly Rate", "created_date-Created Date"]
            
        if view_name == "forms": 
            systemviewps.table_name.set("sys_new_dynamic_form")
            colarray = ["form_id-Form ID", "form_name-Form Name", "created_by-Created By", "created_date-Created Date"]

        if view_name == "scopeofwork": 
            systemviewps.table_name.set("sys_new_dynamic_form")
            colarray = ["form_id-Form ID", "form_name-Form Name", "created_by-Created By", "created_date-Created Date"]
            # $colarray = array("scope_id-Scope ID", "op_scope_name-Operational Scope Name-Text", "scope_name-Customer Scope Name-Text", "sow_tat-Turn Around Time", "min_cost~AMT-Min. Cost", "scope_cost~AMT-Cost", "list_total~AMT-List Cost", "is_lock-Locked");
        
        if view_name == "dynamicview": 
            systemviewps.table_name.set("sys_new_dynamic_view")
            colarray = ["view_id-ID", "view_name-View Name", "url-URL", "created_by-Created By", "created_date-Created Date"]
        
        systemviewps.colarray.set(colarray)
        item_data = getSystemView(systemviewps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Data List",

                # page_title = "Scope of Work",
                # allow_add = "1",
                # allow_view = "1",
                # allow_edit = "1",
                # allow_delete = "1",
                
                # table_name = "scopeofwork"
                # primary_key_name = "scope_id"
                
                # Title, btn_icon, btn_class, btn_url (Json)
                # $extraaction = array("scopeofwork.processtest|Link Process Test|btn-primary|shuffle", "scopeofwork.duplicate|Duplicate|btn-info|copy");
                # $enabledelete = '1',  Pending
                # left_tblname = "", Pending
                # has_child = "", Pending
                # $scopetests = DB::table('lims_scope_tests')
                                #                     ->select('lims_scope_tests.*', 'lims_test_master.name', 'lims_test_master.testtype', 'lims_test_master.target')
                                #                     ->leftJoin('lims_test_master', 'lims_test_master.test_id', '=', 'lims_scope_tests.test_id')
                                #                     ->where('lims_scope_tests.is_delete', 0)
                                #                     ->orderBy('rank', 'ASC')
                                #                     ->get();
                # $childlayout = "scopeofwork.scopetestlist";

                "rcdcnt": systemviewps.rcdcnt.get(),
                "item_data": item_data,
            }
        )
    except Exception as e:
        saveErrorLogtoDB("System View", 0, "getSystemViewList", str(e))
        raiseAPIError(str(e), 500)