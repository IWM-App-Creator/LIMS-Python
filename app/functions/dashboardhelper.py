import json

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