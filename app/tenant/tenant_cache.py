from sqlalchemy import select
from app.dbhelper.db_helper import DB

class TenantCache:

    _ws_cache = {}
    @classmethod
    def get_workspace(cls, subdomain):
        # print("get_workspace --> ", subdomain)
        if subdomain in cls._ws_cache:
            return cls._ws_cache[subdomain]
        workspace_master = DB.get_table("workspace_master", "systemconfig").alias("ws")
        stmt = (
            select(workspace_master)
                .where(workspace_master.c.ws_url == subdomain)
                .where(workspace_master.c.is_delete == 0)
        )
        # print("stmt --> ", stmt)
        row = DB.select_one(stmt)
        if row:
            cls._ws_cache[subdomain] = row
        return row