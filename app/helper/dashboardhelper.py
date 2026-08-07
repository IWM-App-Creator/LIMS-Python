import json
from app.dbfunctions.dashboardfunctions import getDashboardData, insertUpdateDashboard

def getUserDashboards(dps):
    dashboards = getDashboardData(dps)
    dashboards_data = []
    for dash in dashboards:
        if getattr(dash, "is_active", 0) in ("1", 1):
            dps.dashboard_id.set(getattr(dash, "dashboard_id", ""))
            dps.dashboard_name.set(getattr(dash, "dashboard_name", ""))
        row = {
            "dashboard_id": dash.dashboard_id,
            "dashboard_name": dash.dashboard_name,
            "is_active": dash.is_active
        }
        dashboards_data.append(row)
    dps.dashboards_data.set(dashboards_data)

def saveUserDashboards(dps):
    insertUpdateDashboard(dps)
