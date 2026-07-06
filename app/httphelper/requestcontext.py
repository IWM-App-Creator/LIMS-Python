from fastapi import Request
from fastapi.responses import JSONResponse
from app.httphelper.publicendpoints import isPublicEndpoint
from app.tenant.tenant_cache import TenantCache
from app.properties.usersproperties import userps

async def request_context(request: Request, call_next):
    # print("request_context --> ")
    # Skip public APIs
    if isPublicEndpoint(request.url.path):
        return await call_next(request)
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
    # Validate Workspace
    # --------------------------
    TenantCache.cacheTenantWS()
    if userps.workspace_id.get() is None or userps.workspace_id.get() == "":
        return JSONResponse (
            status_code = 404,
            content = {
                "status": False,
                "message": "Workspace not found"
            }
        )
    # --------------------------
    # Output
    # --------------------------
    response = await call_next(request)
    return response