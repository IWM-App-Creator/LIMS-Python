from app.properties.usersproperties import userps
from app.dbfunctions.workspacefunctions import getWorkspaceData
from app.properties.workspaceproperties import wsps

class TenantCache:

    _ws_cache = {}

    @classmethod
    def cacheTenantWS(cls):
        cachekey = (userps.req_subdomain.get(), userps.user_id.get())
        workspace = cls._ws_cache.get(cachekey)
        if workspace is None:
            wsps.domain_flag.set(1)
            wsps.fetch_single.set(1)
            getWorkspaceData(wsps)
            workspace = wsps.ws_data.get()
            if workspace:
                cls._ws_cache[cachekey] = workspace # Save User Wise WS In Cache
        # If Data found, Set Into Context Property
        if workspace:
            userps.workspace_id.set(workspace.workspace_id)
            userps.workspace_name.set(workspace.workspace_name)
            userps.ws_url.set(workspace.ws_url)
            userps.schema_name.set(workspace.schema_name)
            userps.ws_role_id.set(workspace.ws_role_id)

    @classmethod
    def clearWorkSpaceCache(cls, subdomain = None, user_id = None):
        subdomain = subdomain or userps.req_subdomain.get()
        user_id = user_id or userps.user_id.get()
        cachekey = (subdomain, user_id)
        cls._ws_cache.pop(cachekey, None)