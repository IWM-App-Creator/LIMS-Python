from contextvars import ContextVar

class viewproperties:
    def __init__(self):
        self.userview = ContextVar("userview", default = [])

        self.call_from = ContextVar("call_from", default = "")

        self.view_id = ContextVar("view_id", default = "")
        self.view_name = ContextVar("view_name", default = "")
        self.view_url = ContextVar("view_url", default = "")
        self.view_type = ContextVar("view_type", default = "")

        self.tab_id = ContextVar("tab_id", default = "")
        self.page_no = ContextVar("page_no", default = "")
        self.txtsearch = ContextVar("txtsearch", default = "")
        self.filterqry = ContextVar("filterqry", default = "")

        self.view_options = ContextVar("view_options", default = [])
        self.view_cols = ContextVar("view_cols", default = [])
        self.view_joins = ContextVar("view_joins", default = [])
        self.view_child = ContextVar("view_child", default = [])
        self.view_actions = ContextVar("view_actions", default = [])

viewps = viewproperties()