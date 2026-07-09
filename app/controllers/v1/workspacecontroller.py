from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError
from app.dbfunctions.workspacefunctions import isWorkspaceValid

def getWorkspaceList (request: Request):
    # wsps.domain_flag.set(0)
    # wsps.fetch_single.set(0)
    # getWorkspaceData(wsps)
    # setWorkspaceOutput(wsps)
    # return JSONResponse (
    #     status_code = 200,
    #     content = {
    #         "status": True,
    #         "message": "User Data",
    #         "ws_list" : wsps.ws_data.get(),
    #     }
    # )
    print("getTestData --> ")

def isWSValid (subdomain: str):
    workspace_id = isWorkspaceValid(subdomain) # Execute Function to User WS Data
    if workspace_id == "0" : # Invalid Workspace
        raiseAPIError("Invalid Workspace", 401)
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "Valid Workspace",
            "workspace_id": workspace_id
        }
    )