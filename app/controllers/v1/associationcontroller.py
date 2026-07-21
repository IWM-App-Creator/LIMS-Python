from app.utils.common import Request, RequestData, JSONResponse
from app.helper.associationhelper import getAssociationList, getLookupDataByAssociationId, getDesignationList
from app.helper.customviewhelper import getCustomViewList
from app.helper.menuhelper import getUserMenuList
from app.dbfunctions.workspacefunctions import getWorkspaceData
from app.properties.associationproperties import associationps
from app.properties.workspaceproperties import wsps
from app.properties.customviewproperties import customvwps
from app.properties.menuproperties import menups

def getAssociations(request: Request):
    params = RequestData.params(request)
    flag = params.get("flag", "")
    wsps.workspace_id.set(params.get("workspace_id", ""))
    ws_data = getWorkspaceData(wsps)
    if ws_data not in (None, "", {}, 0):
        associationps.schema_name.set(ws_data.schema_name)
        customvwps.schema_name.set(ws_data.schema_name)
        menups.schema_name.set(ws_data.schema_name)
    if flag == "" or flag == "AssociationList":
        associations = getAssociationList(associationps)
    if flag == "" or flag == "DesignationList":
        designations = getDesignationList(associationps)
    customview_list = getCustomViewList(customvwps)
    menups.created_by.set(None)
    menups.m_centre_id.set(None)
    menups.is_active.set(None)
    menups.is_public.set(1)
    getUserMenuList(menups)
    return JSONResponse(
        status_code = 200,
        content = {
            "status": True,
            "message": "Association List",
            "association_list": associations,
            "designation_list": designations,
            "customview_list": customview_list,
            "menu_list": menups.menu_cntr_data.get()
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
            "association_access": association_access
        }
    )