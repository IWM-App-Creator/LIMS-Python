import json
from app.dbfunctions.dashboardfunctions import getDashboardData

def getUserDashboards(dps):
    dashboards = getDashboardData(dps)
    dashboards_data = []
    for dash in dashboards:
        row = {
            "dashboard_id": dash.dashboard_id,
            "dashboard_name": dash.dashboard_name,
            "is_active": dash.is_active
        }
        dashboards_data.append(row)
    dps.dashboards_data.set(dashboards_data)