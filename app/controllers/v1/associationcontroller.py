from app.utils.common import Request, RequestData, JSONResponse
from app.helper.associationhelper import getAssociationList
from app.dbfunctions.workspacefunctions import getWorkspaceData
from app.properties.associationproperties import associationps
from app.properties.workspaceproperties import wsps

def getAssociations(request: Request):
    params = RequestData.params(request)
    wsps.workspace_id.set(params.get("workspace_id", ""))
    ws_data = getWorkspaceData(wsps)
    if ws_data not in (None, "", {}):
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
