from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError, userps
from app.dbfunctions.workspacefunctions import isWorkspaceValid, getWorkspaceData
from app.helper.workspacehelper import setWorkspaceOutput
from app.properties.workspaceproperties import wsps

def getWorkspaceList (request: Request):
    wsps.domain_flag.set(0)
    wsps.fetch_single.set(0)

    userps.user_id.set(3779) # Temp
    getWorkspaceData(wsps)
    setWorkspaceOutput(wsps)
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "Work Space Data",
            "ws_list" : wsps.ws_data.get(),
        }
    )

def isWSValid (subdomain: str):
    # IF auth. Calling validateWorkspace -->
    workspace_id = isWorkspaceValid(subdomain) # Execute Function to User WS Data
    if workspace_id == "0" and subdomain != "auth" : # Invalid Workspace
        return JSONResponse (
            status_code = 200,
            content = {
                "status": False,
                "message": "Valid Workspace",
                "workspace_id": workspace_id
            }
        )
    #     raiseAPIError("Invalid Workspace", 401)
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "Valid Workspace",
            "workspace_id": workspace_id
        }
    )