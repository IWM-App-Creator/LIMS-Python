from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError
from app.dbfunctions.workspacefunctions import isWorkspaceValid

def getWorkspaceList (request: Request):
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