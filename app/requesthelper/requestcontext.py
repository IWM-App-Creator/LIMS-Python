import os
from fastapi import Request
from fastapi.responses import JSONResponse
from app.tenant.tenant_cache import TenantCache

async def request_context(request: Request, call_next):
    # --------------------------
    # Request Headers & JWT
    # --------------------------
    request.state.headers = dict(request.headers)
    request.state.jwt = request.headers.get("Authorization")
    # --------------------------
    # Request Parameters
    # --------------------------
    if request.method == "GET":
        request.state.params = dict(request.query_params)
    else:
        content_type = request.headers.get("Content-Type", "")
        if "application/json" in content_type:
            request.state.params = await request.json()
        else:
            request.state.params = dict(await request.form())

    # --------------------------
    # Workspace
    # --------------------------
    print("Debug IS_LOCAL_DEV --> ", os.getenv('IS_LOCAL_DEV'))
    # print(os.getenv("IS_LOCAL_DEV"))

    host = request.headers.get("Host", "")
    # print("Debug host --> ", host)
    # Remove port if present
    host = host.split(":")[0]

    # print("Debug host 2 --> ", host)
    # Example:
    # customer1.example.com -> customer1
    # localhost -> localhost
    subdomain = host.split(".")[0]
    # print("Debug subdomain --> ", subdomain)
    
    
    if os.getenv('IS_LOCAL_DEV') is 1 :
        subdomain = os.getenv('LOCAL_SUBDOMAIN')
        # print("Debug subdomain 2 --> ", subdomain)
    
    # print("request_context subdomain --> ", subdomain)

    workspace = TenantCache.get_workspace(subdomain)
    if workspace is None:
        return JSONResponse (
            status_code = 404,
            content = {
                "status": False,
                "message": "Workspace not found"
            }
        )
    request.state.workspace = workspace
    request.state.schema = workspace.schema_name
    request.state.workspace_id = workspace.workspace_id
    # --------------------------
    response = await call_next(request)
    return response