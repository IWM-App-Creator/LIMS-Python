from sqlalchemy import select
from app.dbhelper.db_helper import DB

class TenantCache:

    _ws_cache = {}
    @classmethod
    def cacheTenantWS(cls, subdomain):
        if subdomain in cls._ws_cache:
            return cls._ws_cache[subdomain]
        workspace_master = DB.getTableMeta("workspace_master", "systemconfig").alias("ws")
        stmt = (
            select(workspace_master)
                .where(workspace_master.c.ws_url == subdomain)
                .where(workspace_master.c.is_delete == 0)
        )
        row = DB.executeDBSelectSingle(stmt)
        if row:
            cls._ws_cache[subdomain] = row
        return row
    


    # $userdtlarr = DB::table('systemconfig.users')
    #                     ->select('users.*', 'workspace_master.workspace_id', 'workspace_master.workspace_name', 'workspace_master.ws_url', 'workspace_master.schema_name', 'workspace_master.is_setup', 'users_workspace.ws_role_id')
    #                     ->leftJoin('systemconfig.users_workspace', 'users_workspace.user_id', '=', 'users.id')
    #                     ->leftJoin('systemconfig.workspace_master', 'workspace_master.workspace_id', '=', 'users_workspace.workspace_id')
    #                     ->where('id', $user_id)
    #                     ->where('ws_url', $ws_url)
    #                     ->where('api_secret', $api_secret)
    #                     ->first();
    #         if($userdtlarr && $changedb == 1) {
    #             $active_db = $userdtlarr->schema_name;
    #             $mysqlConn = DB::connection();
    #             $mysqlConn->getPdo()->exec("USE " . $active_db);
    #             $mysqlConn->setDatabaseName($active_db);
    #         }