from contextvars import ContextVar

class viewlayoutproperties:
    def __init__(self):
        self.call_from = ContextVar("call_from", default = "")

        self.srno = ContextVar("srno", default = 0)
        self.view_id = ContextVar("view_id", default = 0)
        self.tab_id = ContextVar("tab_id", default = 0)
        self.col_flag = ContextVar("col_flag", default = "")
        self.key_flag = ContextVar("key_flag", default = "")
        self.key_val = ContextVar("key_val", default = "")
        self.rm_flag = ContextVar("rm_flag", default = "")

        self.lydata = ContextVar("lydata", default = {})
        self.db_upd_vals = ContextVar("db_upd_vals", default = {})

viewlyps = viewlayoutproperties()