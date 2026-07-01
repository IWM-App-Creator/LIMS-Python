# host = request.headers.get("host")

# subdomain = host.split(".")[0]

# workspace = TenantCache.get_workspace(subdomain)

# if workspace is None:
#     return JSONResponse(
#         status_code=404,
#         content={
#             "status": False,
#             "message": "Workspace not found"
#         }
#     )

# request.state.workspace = workspace
# request.state.workspace_id = workspace.workspace_id
# request.state.schema = workspace.schema_name