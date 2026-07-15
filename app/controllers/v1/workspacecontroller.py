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

# http://testws1.localhost:8000/api/v1/workspace/save?workspace_id=6&workspace_name=abc&ws_url=&size_limit=2048
# http://testws1.localhost:8000/api/v1/workspace/save?workspace_id=&workspace_name=New WS&ws_url=newws1&size_limit=2048

async def saveWorkspace(request: Request):
    try:
        params = RequestData.params(request)
        wsps.workspace_id.set(params.get("workspace_id", 0) )
        wsps.workspace_name.set(params.get("workspace_name", "") )
        wsps.ws_url.set(params.get("ws_url", "") )
        wsps.size_limit.set(params.get("size_limit", "") )
        ws_logo_file = await RequestData.file(request, "ws_logo") # Get Media 
        wsps.ws_logo_file.set(ws_logo_file)
        if wsps.workspace_id.get():
            updateWorkspace(wsps)
        else:
            wsfnct.getSingleWorkspaceData(wsps) # Get Workspace by URL
            wsdata = wsps.ws_data.get()
            if wsdata is None:
                createWorkspace(wsps)
            else:
                raiseAPIError(wsps.ws_url.get() + "Workspace URL Already Exist, Please Enter Different Workspace URL", 200)
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

