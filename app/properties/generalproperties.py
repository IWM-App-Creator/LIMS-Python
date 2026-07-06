from contextvars import ContextVar

class GeneralProperties:
    def __init__(self):
        self.user_id = ContextVar("user_id", default = "")
        self.role_id = ContextVar("role_id", default = "")
        self.ws_role_id = ContextVar("ws_role_id", default = "")
        # itmjson
        # self.view_col_type = ContextVar("view_col_type", default={})

userps = GeneralProperties()