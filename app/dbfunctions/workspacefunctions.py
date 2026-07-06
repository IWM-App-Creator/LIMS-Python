from sqlalchemy import select
from app.dbhelper.db_helper import DB
from app.properties.usersproperties import userps
    
def getWorkspaceData():
    workspace_master = DB.getTableMeta("workspace_master", "systemconfig").alias("ws")
    users_workspace = DB.getTableMeta("users_workspace", "systemconfig").alias("wsusr")
    stmt = (
        select(
            workspace_master.c.workspace_id,
            workspace_master.c.workspace_name,
            workspace_master.c.ws_url,
            workspace_master.c.schema_name,
            users_workspace.c.ws_role_id
        )
        .join(
            users_workspace,
            users_workspace.c.workspace_id == workspace_master.c.workspace_id,
        )
        .where(workspace_master.c.ws_url == userps.req_subdomain.get())
        .where(workspace_master.c.is_delete == 0)
        .where(users_workspace.c.ws_role_id < 3)
        .where(users_workspace.c.is_delete == 0)
        .where(users_workspace.c.user_id == userps.user_id.get())
    )
    workspace = DB.executeDBSelectSingle(stmt)
    return workspace

def getWorkspaceActiveURL():
    workspace_master = DB.getTableMeta("workspace_master", "systemconfig").alias("ws")
    stmt = (
        select(workspace_master.c.ws_url)
        .where(workspace_master.c.workspace_id == userps.workspace_id.get())
        .limit(1)
    )
    row = DB.executeDBSelectSingle(stmt)
    if row:
        return row.ws_url
    return ""

def isWorkspaceValid(subdomain: str):
    ws_url = subdomain
    if subdomain == "" :
        ws_url = userps.ws_url.get()

    workspace_master = DB.getTableMeta("workspace_master", "systemconfig").alias("ws")
    stmt = (
        select(workspace_master.c.workspace_id)
        .where(workspace_master.c.ws_url == ws_url)
        .limit(1)
    )
    row = DB.executeDBSelectSingle(stmt)
    if row:
        return row.workspace_id
    return "0"