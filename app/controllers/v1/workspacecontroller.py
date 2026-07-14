from app.utils.common import DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, nowWithTimeZone, userps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
import app.dbfunctions.workspacefunctions as wsfn
from app.helper.workspacehelper import setWorkspaceOutput
from app.properties.workspaceproperties import wsps

# http://testws1.localhost:8000/api/v1/workspace/isvalidws?subdomain=testws1
def isWSValid (subdomain: str):
    workspace_id = wsfn.isWorkspaceValid(subdomain) # Execute Function to User WS Data
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
        wsfn.getWSListByUsers(wsps)
        setWorkspaceOutput(wsps)
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
def getUserWorkspaceList(request: Request):
    try:
       print("")
    except Exception as e:
        saveErrorLogtoDB ("Workspace", 0, "getWorkspaceList", str(e))
        raiseAPIError(str(e), 500)
