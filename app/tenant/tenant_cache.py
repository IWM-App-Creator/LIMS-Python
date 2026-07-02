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
        # return


        # row = DB.executeDBSelectSingle(stmt)
        if row:
            cls._ws_cache[subdomain] = row
        return row

    # $userdtlarr = DB::table('systemconfig.users')
    #                     ->select('users.*', 'workspace_master.workspace_id', 'workspace_master.workspace_name', 'workspace_master.ws_url', 'workspace_master.schema_name', 'workspace_master.is_setup', 'users_workspace.ws_role_id')
    #                     ->leftJoin('systemconfig.users_workspace', 'users_workspace.user_id', '=', 'users.id')
    #                     ->leftJoin('systemconfig.workspace_master', 'workspace_master.workspace_id', '=', 'users_workspace.workspace_id')
    #                     ->where('id', $user_id)
    #                     ->where('ws_url', $ws_url)
    #                     ->first();