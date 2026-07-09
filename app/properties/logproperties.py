from contextvars import ContextVar

class LogProperties:
    def __init__(self):
        self.error_id = ContextVar("error_id", default = 0)
        self.item_id = ContextVar("item_id", default = "")
        self.section = ContextVar("section", default = "")
        self.page_no = ContextVar("page_no", default = 1)
        self.page_size = ContextVar("page_size", default = 5)
        self.logdata = ContextVar("logdata", default = [])        
        self.total_record = ContextVar("total_record", default = 0)
        
logps = LogProperties()