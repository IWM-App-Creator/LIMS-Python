from contextvars import ContextVar

class DashboardProperties:
    def __init__(self):
        self.dashboard_id = ContextVar("dashboard_id", default = 0)
        self.dashboard_name = ContextVar("dashboard_name", default = "")
        self.is_active = ContextVar("is_active", default = 0)

        self.dashboards_data = ContextVar("dashboards_data", default = [])
        self.fetch_single = ContextVar("fetch_single", default = 0)

dps = DashboardProperties()