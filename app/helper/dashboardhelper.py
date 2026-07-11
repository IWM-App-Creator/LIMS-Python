import json
from app.dbfunctions.dashboardfunctions import getUserDashboards

def setDashboardOutput(dps):
    dash_arr = dps.dashboards_data.get()
    dashboards_data = []
    for dashboard in dash_arr:
        row = {
            "dashboard_id": dashboard.dashboard_id,
            "dashboard_name": dashboard.dashboard_name,
            "is_active": dashboard.is_active
        }
        dashboards_data.append(row)
    dps.dashboards_data.set(dashboards_data)

def getActiveDashboard(dps):
    dash_arr = dps.dashboards_data.get()
    for act_dash in dash_arr:
        if act_dash.is_active == 1:
            dps.active_dash_id.set(act_dash.dashboard_id)