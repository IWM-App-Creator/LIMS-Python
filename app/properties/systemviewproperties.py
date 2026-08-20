from contextvars import ContextVar

class SystemViewProperties:
    def __init__(self):
        self.view_name = ContextVar("view_name", default = "")
        self.page_no = ContextVar("page_no", default = 1)
        self.filter_qry = ContextVar("filter_qry", default = "")
        self.search_text = ContextVar("search_text", default = "")
        self.table_name = ContextVar("table_name", default = "")
        self.colarray = ContextVar("colarray", default = [])

        self.page_size = ContextVar("page_size", default = 10)
        self.rcdcnt = ContextVar("rcdcnt", default = 0)

systemviewps = SystemViewProperties()