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
        colarray = ["expense_id", "expense_name", "rate", "created_date"]
        if view_name == "labour": 
            systemviewps.table_name.set("lims_labour_master")
            colarray = ["labour_id", "labour_name", "hourly_rate", "created_date"]
            # // $extraaction = array("process.calculations|Calculations|btn-primary|dollar-sign", "processes.duplicate|Duplicate|btn-info|copy");
            # allow add... 
            # $showurl = ''; //'processes.show';
            # $editurl = 'processes.edit';
            # $enabledelete = '1';
            # $destroyurl = 'processes.destroy';
            # has_child.. / child_view_name


        systemviewps.colarray.set(colarray)
        item_data = getSystemView(systemviewps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Data List",
                "rcdcnt": systemviewps.rcdcnt.get(),
                "item_data": item_data
            }
        )
    except Exception as e:
        saveErrorLogtoDB("System View", 0, "getSystemViewList", str(e))
        raiseAPIError(str(e), 500)