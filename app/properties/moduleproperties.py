from contextvars import ContextVar

class ModuleProperties:
    def __init__(self):
        self.template_id = ContextVar("template_id", default = None)
        self.template_name = ContextVar("template_name", default = None)
        self.template_type = ContextVar("template_type", default = None)
        self.table_data = ContextVar("table_data", default = None)
        self.t_cat_id = ContextVar("t_cat_id", default = None)
        self.s_desc = ContextVar("s_desc", default = None)
        self.l_desc = ContextVar("l_desc", default = None)

moduleps = ModuleProperties()
# template_id, template_name, template_type, table_data, t_cat_id, s_desc, l_desc, status_1, is_delete, created_by, is_metadata, created_date