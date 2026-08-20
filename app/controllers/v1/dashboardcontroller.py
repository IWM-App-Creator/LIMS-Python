from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.dashboardfunctions import insertUpdateDashboard
from app.helper.generalfunctions import normalizeJson
from app.properties.dashboardproperties import dps

# [
#     {
#         "dashboard_id": 1,
#         "dashboard_name": "Default",
#         "is_active": 0,
#         "isDeleted": false,
#         "isNew": false
#     },
#     {
#         "dashboard_id": 16,
#         "dashboard_name": "Rushi's Dash",
#         "is_active": 1,
#         "isDeleted": false,
#         "isNew": false
#     },
#     {
#         "dashboard_id": 17,
#         "dashboard_name": "New Dashboard",
#         "is_active": 0,
#         "isDeleted": true,
#         "isNew": false
#     },
#     {
#         "dashboard_id": -1,
#         "dashboard_name": "RKO Dash",
#         "is_active": 0,
#         "isNew": true,
#         "isDeleted": false
#     }
# ]
def saveUserDashboard(request: Request):
    print("saveUserDashboard --> ")
    try:
        params = RequestData.params(request)
        dashboards = normalizeJson(params.get("dashboards", []), [])
        if not isinstance(dashboards, list):
            dashboards = []
        for dash in dashboards:
            dps.db_upd_vals.set(None)
            dps.dashboard_name.set(None)
            dps.is_active.set(None)
            if not isinstance(dash, dict):
                continue
            if dash.get("isNew") in ("true", True) and dash.get("isDeleted") in ("false", False):
                dps.dashboard_name.set(dash.get("dashboard_name", ""))
                dps.is_active.set(dash.get("is_active", ""))
            elif dash.get("isDeleted") in ("true", True) and dash.get("isNew") in ("false", False):
                dps.dashboard_id.set(dash.get("dashboard_id", ""))
                dps.db_upd_vals.set({"is_delete": 1})
            else:
                dps.dashboard_id.set(dash.get("dashboard_id", ""))
                dps.dashboard_name.set(dash.get("dashboard_name", ""))
                dps.is_active.set(dash.get("is_active", ""))
            insertUpdateDashboard(dps)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Dashboard Saved Successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Dashboard", userps.user_id.get(), "saveUserDashboard", str(e))
        raiseAPIError(str(e), 500)