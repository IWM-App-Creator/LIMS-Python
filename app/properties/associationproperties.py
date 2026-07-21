from contextvars import ContextVar

class AssociationProperties:

    def __init__(self):
        self.associations_id = ContextVar("associations_id", default = "")
        self.designation_id = ContextVar("designation_id", default = "")

        self.view_id = ContextVar("view_id", default = 0)
        self.view_ids = ContextVar("view_ids", default = "")

        self.user_id = ContextVar("user_id", default = 0)
        self.col_id = ContextVar("col_id", default = 0)
        self.col_p_val = ContextVar("col_p_val", default = 0)
        self.col_p_vals = ContextVar("col_p_vals", default = [])

        self.access_json = ContextVar("access_json", default = {})
        self.is_owner = ContextVar("is_owner", default = 0)
        self.is_edit = ContextVar("is_edit", default = 0)
        self.is_view = ContextVar("is_view", default = 0)
        self.is_noaccess = ContextVar("is_noaccess", default = 0)
        self.dyncviews = ContextVar("dyncviews", default = "")
        self.custlink = ContextVar("custlink", default = "")
        self.menucntr = ContextVar("menucntr", default = "")
        self.modules = ContextVar("modules", default = "")
        self.dashboardcntr = ContextVar("dashboardcntr", default = "")
        self.defmenucntr = ContextVar("defmenucntr", default = 0)
        self.defdashboard = ContextVar("defdashboard", default = 0)

        self.table_name = ContextVar("table_name", default = "")
        self.pcol_id = ContextVar("pcol_id", default = "")
        self.pcol_nm = ContextVar("pcol_nm", default = "")
        self.lcol_nm = ContextVar("lcol_nm", default = "")
        self.txtsearch = ContextVar("txtsearch", default = "")
        self.pgno = ContextVar("pgno", default = 1)

        self.ass_users_data = ContextVar("ass_users_data", default = [])

        self.schema_name = ContextVar("schema_name", default = None)
        self.fetch_single = ContextVar("fetch_single", default = 0)
        self.is_distinct = ContextVar("is_distinct", default = 0)

associationps = AssociationProperties()