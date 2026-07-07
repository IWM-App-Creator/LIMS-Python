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

        # viewps.table_id.set(viewopt.get("table_id", 0))
        # viewps.table_name.set(viewopt.get("table_name", 0))
        # viewps.view_qry.set(viewopt.get("view_qry", 0))
        # viewps.primary_col.set(viewopt.get("primary_col", 0))
        # viewps.primary_col.set(viewopt.get("primary_col", 0))
        # viewps.delete_col.set(viewopt.get("delete_col", 0))
        # viewps.show_deleted.set(viewopt.get("show_deleted", 0))
        # viewps.enable_newline.set(viewopt.get("enable_newline", 0))
        # viewps.enable_join_save.set(viewopt.get("enable_join_save", 0))
        # viewps.is_child_view.set(viewopt.get("is_child_view", 0))
        # viewps.enable_child_srch.set(viewopt.get("enable_child_srch", 0))
        # viewps.enable_chart.set(viewopt.get("enable_chart", 0))

viewps = viewproperties()