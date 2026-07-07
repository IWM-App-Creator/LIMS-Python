from contextvars import ContextVar

class LogProperties:
    def __init__(self):
        self.error_id = ContextVar("error_id", default = 0)
        self.view_id = ContextVar("view_id", default = "")
        self.log_type = ContextVar("log_type", default = "")
        self.section = ContextVar("section", default = "")
        self.desc = ContextVar("desc", default = "")
        self.error_msg = ContextVar("error_msg", default = "")

logps = LogProperties()