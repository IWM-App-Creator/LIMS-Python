from contextvars import ContextVar

class SystemViewProperties:
    def __init__(self):
        self.table_name = ContextVar("table_name", default = "")
        self.schema_name = ContextVar("schema_name", default = None)

systemviewps = SystemViewProperties()