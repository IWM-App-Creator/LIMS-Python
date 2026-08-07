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

        systemviewps.table_name.set("lims_expense_master") # temporary default, if no mapping table found redirect to 404..
        colarray = ["expense_id-Expense ID", "expense_name-Expense Name", "rate-Rate", "created_date-Created Date"]
        if view_name == "labour": 
            systemviewps.table_name.set("lims_labour_master")
            colarray = ["labour_id-Labour ID", "labour_name-Labour Name", "hourly_rate-Hourly Rate", "created_date-Created Date"]
            
        if view_name == "forms": 
            systemviewps.table_name.set("sys_new_dynamic_form")
            colarray = ["form_id-Form ID", "form_name-Form Name", "created_by-Created By", "created_date-Created Date"]

        systemviewps.colarray.set(colarray)
        item_data = getSystemView(systemviewps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Data List",
                # // $extraaction = array("process.calculations|Calculations|btn-primary|dollar-sign", "processes.duplicate|Duplicate|btn-info|copy");
                # allow add... 
                # $showurl = ''; //'processes.show';
                # $editurl = 'processes.edit';
                # $enabledelete = '1';
                # $destroyurl = 'processes.destroy';
                # has_child.. / child_view_name
                "rcdcnt": systemviewps.rcdcnt.get(),
                "item_data": item_data
            }
        )
    except Exception as e:
        saveErrorLogtoDB("System View", 0, "getSystemViewList", str(e))
        raiseAPIError(str(e), 500)