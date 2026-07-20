from app.utils.common import Request, RequestData, JSONResponse
from app.helper.associationhelper import getAssociationList, getLookupDataByAssociationId
from app.dbfunctions.workspacefunctions import getWorkspaceData
from app.properties.associationproperties import associationps
from app.properties.workspaceproperties import wsps

def getAssociations(request: Request):
    params = RequestData.params(request)
    wsps.workspace_id.set(params.get("workspace_id", ""))
    ws_data = getWorkspaceData(wsps)
    if ws_data not in (None, "", {}, 0):
        associationps.schema_name.set(ws_data.schema_name)
    associations = getAssociationList(associationps)
    return JSONResponse(
        status_code = 200,
        content = {
            "status": True,
            "message": "Association List",
            "associations": associations
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