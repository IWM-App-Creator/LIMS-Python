from contextvars import ContextVar

class viewproperties:
    def __init__(self):
        self.userview = ContextVar("userview", default = [])
        self.call_from = ContextVar("call_from", default = "")
        self.view_id = ContextVar("view_id", default = "0")
        self.view_name = ContextVar("view_name", default = "")
        self.view_url = ContextVar("view_url", default = "")
        self.view_type = ContextVar("view_type", default = "")
        self.view_qry = ContextVar("view_qry", default = "")

        self.tab_id = ContextVar("tab_id", default = "0")
        self.page_no = ContextVar("page_no", default = "")
        self.txtsearch = ContextVar("txtsearch", default = "")
        self.filterqry = ContextVar("filterqry", default = "")

        self.view_options = ContextVar("view_options", default = [])
        self.view_cols = ContextVar("view_cols", default = [])
        self.tbl_cols = ContextVar("tbl_cols", default = [])
        self.view_joins = ContextVar("view_joins", default = [])
        self.view_child = ContextVar("view_child", default = [])
        self.view_actions = ContextVar("view_actions", default = [])

        # View Options Properties
        self.table_id = ContextVar("table_id", default = "0")
        self.table_name = ContextVar("table_name", default = "")
        self.primary_col = ContextVar("primary_col", default = "")
        self.primary_colnm = ContextVar("primary_colnm", default = "") 
        self.delete_col = ContextVar("delete_col", default = "")
        self.show_deleted = ContextVar("show_deleted", default = "")
        self.enable_newline = ContextVar("enable_newline", default = "0")
        self.enable_join_save = ContextVar("enable_join_save", default = "0")
        self.is_child_view = ContextVar("is_child_view", default = "0")
        self.enable_child_srch = ContextVar("enable_child_srch", default = "0")
        self.enable_chart = ContextVar("enable_chart", default = "0")

        # View Layout Properties
        self.col_metadata = ContextVar("col_metadata", default = [])
        self.col_colors = ContextVar("col_colors", default = [])
        self.action_group_list = ContextVar("action_group_list", default = [])
        self.user_setting = ContextVar("user_setting", default = [])

viewps = viewproperties()