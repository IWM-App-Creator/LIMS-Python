from contextvars import ContextVar

class DBProperties:
    def __init__(self):
        # Table Properties
        self.table_id = ContextVar("table_id", default = 0)
        self.table_name = ContextVar("table_name", default = "")
        self.table_alias = ContextVar("table_alias", default = "")
        
        # Columns Properties
        self.col_id = ContextVar("col_id", default = 0)
        self.col_name = ContextVar("col_name", default = "")
        self.col_alias = ContextVar("col_name", default = "")
        self.col_key = ContextVar("col_key", default = 0)
        self.datatype = ContextVar("datatype", default = "")
        self.length = ContextVar("length", default = "")
        self.is_mandatory = ContextVar("is_mandatory", default = "")
        self.default_val = ContextVar("default_val", default = "")
        self.is_primary = ContextVar("is_primary", default = "")
        self.is_index = ContextVar("is_index", default = "")

        # All DB Table List & Table Cols
        self.all_db_tables = ContextVar("all_db_tables", default = "")
        self.all_db_tbl_col = ContextVar("all_db_tbl_col", default = "")
        
        # Create Query
        self.create_qry = ContextVar("create_qry", default = "")

        # Alter Query
        self.alter_action = ContextVar("action", default = "")
        self.to_col_name = ContextVar("to_col_name", default = "")
        self.after_col = ContextVar("after_col", default = "")
        self.extra = ContextVar("extra", default = "")
        self.alter_qry = ContextVar("alter_qry", default = "")

        # DB Table Data
        self.db_tbl_data = ContextVar("db_tbl_data", default = [])
        self.table_ids = ContextVar("table_ids", default = [])
        self.col_ids = ContextVar("col_ids", default=[])
        self.is_del_tbl = ContextVar("is_del_tbl", default = "0")
        self.is_del_col = ContextVar("is_del_col", default = "0")

        # View / DB Column Types
        self.view_col_type = ContextVar("view_col_type", default={})
        self.db_col_type = ContextVar("db_col_type", default={})

    

dbps = DBProperties()