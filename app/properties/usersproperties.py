from contextvars import ContextVar
# from dataclasses import dataclass

# @dataclass
class UserProperties:
    # workspace_id: int | None = None
    # user_id: int | None = None
    # req_host: str = ""
    # req_subdomain: str = ""

    def __init__(self):
        self.user_id = ContextVar("user_id", default="")
        self.role_id = ContextVar("user_id", default="")
        self.ws_role_id = ContextVar("user_id", default="")
        self.workspace_id = ContextVar("user_id", default="")
        self.workspace_name = ContextVar("user_id", default="")
        self.ws_url = ContextVar("user_id", default="")
        self.schema_name = ContextVar("user_id", default="")

        self.req_host = ContextVar("user_id", default="")
        self.req_subdomain = ContextVar("user_id", default="")

        self.first_name = ContextVar("user_id", default="")
        self.last_name = ContextVar("user_id", default="")
        self.email = ContextVar("user_id", default="")
        self.user_settings = ContextVar("user_id", default="")

userps = UserProperties()

# usercontext = ContextVar("user_context", default = UserProperties())