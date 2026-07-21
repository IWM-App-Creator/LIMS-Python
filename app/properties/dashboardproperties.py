from contextvars import ContextVar

class DashboardProperties:
    def __init__(self):
        self.dashboard_id = ContextVar("dashboard_id", default = 0)
        self.dashboard_name = ContextVar("dashboard_name", default = "")
        self.is_active = ContextVar("is_active", default = 0)
        self.active_dash_id = ContextVar("active_dash_id", default = 0)
        self.created_by = ContextVar("created_by", default = None)

        self.schema_name = ContextVar("schema_name", default = None)
        self.dashboards_data = ContextVar("dashboards_data", default = [])
        self.fetch_single = ContextVar("fetch_single", default = 0)

        self.db_upd_vals = ContextVar("db_upd_vals", default = {})

dps = DashboardProperties()