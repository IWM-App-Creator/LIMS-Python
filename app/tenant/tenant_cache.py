from sqlalchemy import select
from app.dbhelper.db_helper import DB
from app.properties.globalproperties import globalps

class TenantCache:

    _ws_cache = {}
    @classmethod
    def cacheTenantWS(cls, subdomain):
        print("cacheTenantWS user_id--> ", globalps.user_id)
        if subdomain in cls._ws_cache:
            return cls._ws_cache[subdomain]
    
        if globalps.user_id is None or globalps.user_id == "" :
            workspace_master = DB.getTableMeta("workspace_master", "systemconfig").alias("ws")
            stmt = (
                select(workspace_master)
                    .where(workspace_master.c.ws_url == subdomain)
                    .where(workspace_master.c.is_delete == 0)
            )
        else :
            print("subdomain --> ", subdomain)
            users = DB.getTableMeta("users", "systemconfig").alias("usr")
            workspace_master = DB.getTableMeta("workspace_master", "systemconfig").alias("ws")
            users_workspace = DB.getTableMeta("users_workspace", "systemconfig").alias("wsusr")
            stmt = (
                select(
                    users, # usr.*
                    workspace_master.c.workspace_id,
                    workspace_master.c.workspace_name,
                    workspace_master.c.ws_url,
                    workspace_master.c.schema_name,
                    workspace_master.c.is_setup,
                    users_workspace.c.ws_role_id
                )
                .select_from (
                    users.outerjoin(
                        users_workspace,
                        users_workspace.c.user_id == users.c.id
                    ).outerjoin(
                        workspace_master,
                        workspace_master.c.workspace_id == users_workspace.c.workspace_id
                    )
                )
                .where(users.c.id == globalps.user_id)
                .where(workspace_master.c.ws_url == subdomain)
            )
            print("stmt --> ", stmt)
        row = DB.executeDBSelectSingle(stmt)
        print("row --> ", row)

        if row:
            cls._ws_cache[subdomain] = row
        return row