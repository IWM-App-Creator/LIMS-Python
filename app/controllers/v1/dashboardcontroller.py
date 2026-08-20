from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.dashboardfunctions import insertUpdateDashboard
from app.helper.dashboardhelper import getUserDashboards
from app.helper.generalfunctions import normalizeJson
from app.properties.dashboardproperties import dps

def saveUserDashboard(request: Request):
    print("saveUserDashboard --> ")
    try:
        params = RequestData.params(request)
        dashboards = normalizeJson(params.get("dashboards", []), [])
        if not isinstance(dashboards, list):
            dashboards = []
        for dash in dashboards:
            dps.db_upd_vals.set(None)
            dps.dashboard_id.set(None)
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
            dps.db_upd_vals.set(None)
            dps.dashboard_id.set(None)
            dps.dashboard_name.set(None)
            dps.is_active.set(None)
            dps.created_by.set(userps.user_id.get())
            getUserDashboards(dps)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Dashboard Saved Successfully",
                "dashboard_list" : dps.dashboards_data.get(),
                "active_dashboard": int(dps.dashboard_id.get() or 0) or 0,
                "active_dashboard_name": dps.dashboard_name.get() or ""
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Dashboard", userps.user_id.get(), "saveUserDashboard", str(e))
        raiseAPIError(str(e), 500)