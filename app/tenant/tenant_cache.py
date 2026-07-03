from app.properties.usersproperties import userps
from app.functions.workspacefunctions import getWorkspaceData

class TenantCache:

    _ws_cache = {}

    @classmethod
    def cacheTenantWS(cls):
        print("cacheTenantWS --> ")
        cachekey = (userps.req_subdomain.get(), userps.user_id.get())
        workspace = cls._ws_cache.get(cachekey)
        if workspace is None:
            workspace = getWorkspaceData()
            if workspace:
                cls._ws_cache[cachekey] = workspace
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