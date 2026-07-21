from contextvars import ContextVar

class WorkspaceProperties:
    def __init__(self):
        self.workspace_id = ContextVar("workspace_id", default = 0)
        self.workspace_name = ContextVar("workspace_name", default = "")
        self.ws_url = ContextVar("ws_url", default = "")
        self.schema_name = ContextVar("schema_name", default = None)
        self.ws_logo = ContextVar("ws_logo", default = "")
        self.ws_logo_file = ContextVar("ws_logo_file", default = "")
        self.ai_priority = ContextVar("ai_priority", default = "default")
        self.is_setup = ContextVar("is_setup", default = 0)
        self.size_limit = ContextVar("size_limit", default = 1024)

        self.file_count = ContextVar("file_count", default = 1024)
        self.used_size = ContextVar("used_size", default = 1024)

        self.user_wp_id = ContextVar("user_wp_id", default = 0)
        self.ws_usr_id = ContextVar("user_id", default = 0)
        self.ws_role_id = ContextVar("ws_role_id", default = 2)
        self.is_invited = ContextVar("is_invited", default = 1)
        self.is_accepted = ContextVar("is_accepted", default = 0)

        self.chk_ws_role = ContextVar("chk_ws_role", default = 1)
        self.domain_flag = ContextVar("domain_flag", default = 1)
        self.fetch_single = ContextVar("fetch_single", default = 1)
        self.ws_srch = ContextVar("ws_srch", default = "")
        self.ws_data = ContextVar("ws_output", default = [])

        self.db_upd_vals = ContextVar("db_upd_vals", default = {})
        
wsps = WorkspaceProperties()