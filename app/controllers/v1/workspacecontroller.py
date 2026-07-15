from app.utils.common import DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, nowWithTimeZone, userps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
import app.dbfunctions.workspacefunctions as wsfnct
from app.helper.workspacehelper import getWorkspaceByUser, updateWorkspace, createWorkspace
from app.properties.workspaceproperties import wsps

# http://testws1.localhost:8000/api/v1/workspace/isvalidws?subdomain=testws1
def isWSValid (subdomain: str):
    workspace_id = wsfnct.isWorkspaceValid(subdomain) # Execute Function to User WS Data
    if workspace_id == "0" and subdomain != "auth" : # Invalid Workspace
        return JSONResponse (
            status_code = 200,
            content = {
                "status": False,
                "message": "In-Valid Workspace",
                "workspace_id": workspace_id
            }
        )
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "Valid Workspace",
            "workspace_id": workspace_id
        }
    )

# http://testws1.localhost:8000/api/v1/workspace/getlist?txtsearch=test
def getWorkspaceList(request: Request):
    try:
        params = RequestData.params(request)
        wsps.ws_srch.set(params.get("txtsearch", "") )
        getWorkspaceByUser(wsps)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Workspace List",
                "ws_list" : wsps.ws_data.get(),
            }
        )
    except Exception as e:
        saveErrorLogtoDB ("Workspace", 0, "getWorkspaceList", str(e))
        raiseAPIError(str(e), 500)

# http://testws1.localhost:8000/api/v1/workspace/getlist?txtsearch=test
def saveWorkspace(request: Request):
    try:
        params = RequestData.params(request)
        wsps.workspace_id.set(params.get("workspace_id", 0) )
        wsps.workspace_name.set(params.get("workspace_name", "") )
        wsps.ws_url.set(params.get("ws_url", "") )
        wsps.size_limit.set(params.get("size_limit", 1024) )
        if wsps.workspace_id.get():
            updateWorkspace()
        else:
            createWorkspace()
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Workspace Data Saved Successfully!",
                "workspace_id": wsps.workspace_id.get()
            }
        )
    except Exception as e:
        saveErrorLogtoDB ("Workspace", 0, "getWorkspaceList", str(e))
        raiseAPIError(str(e), 500)

