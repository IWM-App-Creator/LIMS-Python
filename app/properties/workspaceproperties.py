from contextvars import ContextVar

class WorkspaceProperties:
    def __init__(self):
        self.workspace_id = ContextVar("workspace_id", default = 0)
        self.workspace_name = ContextVar("workspace_name", default = "")
        self.workspace_namews_url = ContextVar("ws_url", default = "")
        self.schema_name = ContextVar("schema_name", default = "")
        self.ws_role_id = ContextVar("ws_role_id", default = 0)
        self.is_accepted = ContextVar("is_accepted", default = 0)
        self.user_id = ContextVar("user_id", default = 0)

        self.domain_flag = ContextVar("domain_flag", default = 1)
        self.fetch_single = ContextVar("fetch_single", default = 1)
        self.ws_data = ContextVar("ws_output", default = [])

wsps = WorkspaceProperties()