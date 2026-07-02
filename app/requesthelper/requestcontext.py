import os
from fastapi import Request
from fastapi.responses import JSONResponse
from app.tenant.tenant_cache import TenantCache
from app.properties.globalproperties import globalps

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
    host = request.headers.get("Host", "")
    host = host.split(":")[0]
    subdomain = host.split(".")[0]
    if globalps.IS_LOCAL_DEV == "1":
        subdomain = globalps.LOCAL_SUBDOMAIN

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
    # Output
    # --------------------------
    response = await call_next(request)
    return response