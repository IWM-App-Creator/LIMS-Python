from contextvars import ContextVar

class UserProperties:
    def __init__(self):
        self.user_id = ContextVar("user_id", default = "")
        self.role_id = ContextVar("user_id", default = "")
        self.ws_role_id = ContextVar("user_id", default = "")
        self.workspace_id = ContextVar("user_id", default = "")
        self.workspace_name = ContextVar("user_id", default = "")
        self.ws_url = ContextVar("user_id", default = "")
        self.schema_name = ContextVar("user_id", default = "")

        self.req_host = ContextVar("user_id", default = "")
        self.req_subdomain = ContextVar("user_id", default = "")

        self.first_name = ContextVar("user_id", default = "")
        self.last_name = ContextVar("user_id", default = "")
        self.email = ContextVar("user_id", default = "")
        self.user_settings = ContextVar("user_id", default = "")

userps = UserProperties()