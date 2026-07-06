from contextvars import ContextVar

class UserProperties:
    def __init__(self):
        self.user_id = ContextVar("user_id", default = "")
        self.role_id = ContextVar("role_id", default = "")
        self.ws_role_id = ContextVar("ws_role_id", default = "")
        self.workspace_id = ContextVar("workspace_id", default = "")
        self.workspace_name = ContextVar("workspace_name", default = "")
        self.ws_url = ContextVar("ws_url", default = "")
        self.schema_name = ContextVar("schema_name", default = "")

        self.req_host = ContextVar("req_host", default = "")
        self.req_subdomain = ContextVar("req_subdomain", default = "")

        self.first_name = ContextVar("first_name", default = "")
        self.last_name = ContextVar("last_name", default = "")
        self.email = ContextVar("email", default = "")
        self.user_settings = ContextVar("user_settings", default = "")

userps = UserProperties()