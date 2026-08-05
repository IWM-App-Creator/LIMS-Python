from contextvars import ContextVar

class FilterProperties:
    def __init__(self):
        self.save_id = ContextVar("save_id", default = 0)
        self.save_name = ContextVar("save_name", default = "")
        self.view_id = ContextVar("view_id", default = 0)
        self.view_qry = ContextVar("view_qry", default = [])
        self.view_qry_json = ContextVar("view_qry_json", default = [])
        self.is_default = ContextVar("is_default", default = 0)
        self.is_delete = ContextVar("is_delete", default = 0)
        self.user_id = ContextVar("user_id", default = None)

        self.upd_vals = ContextVar("upd_vals", default = {})
        # save_id, save_name, view_id, tab_id, view_qry, view_qry_json, is_default, is_global, is_delete, created_by, created_date

filterps = FilterProperties()