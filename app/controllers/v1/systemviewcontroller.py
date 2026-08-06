from app.utils.common import JSONResponse, Request, RequestData, raiseAPIError, raiseInvalidError
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.helper.systemviewhelper import getSystemView
from app.properties.systemviewproperties import systemviewps

def getSystemViewList(request: Request):
    try:
        params = RequestData.params(request)
        view_name = params.get("view_name", "")
        systemviewps.view_name.set(view_name)
        # systemviewps.page_no.set(params.get("page_no", 1))
        # systemviewps.filter_qry.set(params.get("filter_qry", ""))
        # systemviewps.systemviewps.set(params.get("systemviewps", ""))

        systemviewps.table_name.set("lims_expense_master") # temporary default, if no mapping table found redirect to 404..
        if view_name == "Labour": 
            systemviewps.table_name.set("lims_labour_master")

        systemviewps.schema_name.set("geno")

        if systemviewps.table_name.get() in (None, ""):
            return raiseInvalidError("Table Name Not Found", 401)
        item_data = getSystemView(systemviewps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Data List",
                "rcdcnt": 100,
                "item_data": item_data
            }
        )
    except Exception as e:
        saveErrorLogtoDB("System View", 0, "getSystemViewList", str(e))
        raiseAPIError(str(e), 500)