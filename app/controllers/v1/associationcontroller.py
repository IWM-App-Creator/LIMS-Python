from app.utils.common import Request, RequestData, JSONResponse
from app.helper.associationhelper import getAssociationList, getLookupDataByAssociationId, getDesignationList
from app.helper.customviewhelper import getCustomViewList
from app.helper.menuhelper import getUserMenuList
from app.helper.dashboardhelper import getUserDashboards
from app.helper.dbtablehelper import getDBTables
from app.helper.modulehelper import getModules
from app.dbfunctions.workspacefunctions import getWorkspaceData
from app.properties.associationproperties import associationps
from app.properties.workspaceproperties import wsps
from app.properties.customviewproperties import customvwps
from app.properties.menuproperties import menups
from app.properties.dashboardproperties import dps
from app.properties.dbproperties import dbps
from app.properties.moduleproperties import moduleps

def getAssociations(request: Request):
    params = RequestData.params(request)
    wsps.workspace_id.set(params.get("workspace_id", ""))
    ws_data = getWorkspaceData(wsps)
    if ws_data not in (None, "", {}, 0):
        associationps.schema_name.set(ws_data.schema_name)
        customvwps.schema_name.set(ws_data.schema_name)
        menups.schema_name.set(ws_data.schema_name)
        dps.schema_name.set(ws_data.schema_name)
        dbps.schema_name.set(ws_data.schema_name)
        associations = getAssociationList(associationps) # get Association List
        designations = getDesignationList(associationps) # get Designation List
        customview_list = getCustomViewList(customvwps) # get Custom View List
        menups.is_public.set(1)
        getUserMenuList(menups) # get User Menu List
        getUserDashboards(dps) # get User Dashboard List
        dbps.is_primary.set(1)
        dbtable_list = getDBTables(dbps)
        module_list = getModules(moduleps) # get Module List
    return JSONResponse(
        status_code = 200,
        content = {
            "status": True,
            "message": "Association List",
            "association_list": associations,
            "designation_list": designations,
            "dbtable_list": dbtable_list,
            "customview_list": customview_list,
            "menu_list": menups.menu_cntr_data.get(),
            "dashboard_list": dps.dashboards_data.get(),
            "module_list": module_list
        }
    )

def getAccessAssociation(request: Request):
    print("getAccessAssociation --> ")
    params = RequestData.params(request)
    associationps.table_name.set(params.get("table_name", ""))
    associationps.pcol_id.set(params.get("pcol_id", ""))
    associationps.pcol_nm.set(params.get("pcol_nm", ""))
    associationps.lcol_nm.set(params.get("lcol_nm", ""))
    associationps.txtsearch.set(params.get("txtsearch", ""))
    associationps.pgno.set(params.get("pgno", 1))
    wsps.workspace_id.set(params.get("workspace_id", ""))
    ws_data = getWorkspaceData(wsps)
    if ws_data not in (None, "", {}, 0):
        associationps.schema_name.set(ws_data.schema_name)
    association_access = getLookupDataByAssociationId(associationps)
    return JSONResponse(
        status_code = 200,
        content = {
            "status": True,
            "message": "Association Access List",
            "association_access": association_access,
            "record_cnt": associationps.record_cnt.get()
        }
    )