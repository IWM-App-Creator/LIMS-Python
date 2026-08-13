import json
import requests
from app.utils.common import Request, RequestData, raiseAPIError, raiseInvalidError, JSONResponse, userps
from app.helper.generalfunctions import getSelectedUsers, generateRandomString, getListJsonVal, updateListJsonVal, removeListJsonVal, normalizeJson
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.notificationfunctions import insertUpdateNotification
from app.dbfunctions.dashboardfunctions import getDashboardData, insertUpdateDashboard
from app.dbfunctions.widgetfunctions import getWidgetData, getWidgetCategoryDB, insertUpdateWidget
from app.helper.widgethelper import getWidgets, getUserWidgets
from app.properties.associationproperties import associationps
from app.properties.notificationproperties import notifyps
from app.properties.dashboardproperties import dps
from app.properties.widgetproperties import widgetps

def getWidgetList(request: Request):
    print("getWidgetList --> ")
    try:
        params = RequestData.params(request)
        widgetps.dashboard_id.set(params.get("dashboard_id", 0))
        widgetps.sys_widget_cat_id.set(params.get("sys_widget_cat_id", None))
        widgetps.widget_type.set(params.get("widget_type", None))
        widgetps.search_text.set(params.get("search_text", None))
        widgetps.pg_no.set(params.get("pg_no", 1))
        widget_list = getWidgets(widgetps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Widget List",
                "rcrd_cnt": widgetps.rcrd_cnt.get(),
                "widget_list": widget_list
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", widgetps.dashboard_id.get(), "getWidgetList", str(e))
        raiseAPIError(str(e), 500)

def getUserWidgetList(request: Request):
    print("getUserWidgetList --> ")
    try:
        params = RequestData.params(request)
        widgetps.dashboard_id.set(params.get("dashboard_id", 0))
        widgetps.sys_widget_id.set(params.get("sys_widget_id", 0))
        widgetps.preview.set(params.get("preview", 0))
        usrwdgt_list = getUserWidgets(widgetps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "User Widget List",
                "userwidget_list": usrwdgt_list
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", userps.user_id.get(), "getUserWidgetList", str(e))
        raiseAPIError(str(e), 500)

def getWidgetCategory(request: Request):
    print("getWidgetCategory --> ")
    try:
        params = RequestData.params(request)
        Category_data = getWidgetCategoryDB()
        widget_categories = []
        for cat in Category_data:
            row = {
                "sys_widget_cat_id": getattr(cat, "sys_widget_cat_id", 0),
                "category_name": getattr(cat, "category_name", ""),
            }
            widget_categories.append(row)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Widget Category List",
                "category_list": widget_categories
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", widgetps.sys_widget_cat_id.get(), "getWidgetCategory", str(e))
        raiseAPIError(str(e), 500)

# api/v1/widget/share?view_id=182&sys_widgets_users_id=1&widget_type=ShareFilter&share_users=1,2,3&save_name=Test Filter
def shareUserWidget(request: Request):
    print("shareUserWidget --> ")
    try:
        params = RequestData.params(request)
        view_id = params.get("view_id", 0)
        dashboard_id = params.get("dashboard_id", 0)
        widget_ref_id = params.get("widget_ref_id", "")
        sys_widgets_users_id = params.get("sys_widgets_users_id", 0)
        widget_type = params.get("widget_type", None)
        message = params.get("message", None)
        save_name = params.get("save_name", None)
        share_users = params.get("share_users", [])
        from_user = params.get("from_user", "")
        # Handle FormData where share_users is JSON string
        if isinstance(share_users, str):
            try:
                share_users = json.loads(share_users)
            except json.JSONDecodeError:
                # Fallback for comma-separated values
                share_users = [
                    {"opt_val": int(x), "type": 0}
                    for x in share_users.split(",")
                    if x.strip()
                ]
        # Ensure it's a list
        if not isinstance(share_users, list):
            share_users = []
        title = ""
        msg_data = ""
        share_users = getSelectedUsers(share_users, view_id)
        if widget_type == "ShareWidget":
            title = from_user + " shared a widget with you."
            msg_data = json.dumps({"dashboard_id": dashboard_id, "widget_ref_id": widget_ref_id})
        elif widget_type == "ShareMenu":
            title = save_name
            message = from_user + ' shared a menu "'  + save_name + '"'
            msg_data = json.dumps({"m_center_id": sys_widgets_users_id})
        elif widget_type == "ShareFilter":
            title = save_name
            message = from_user + ' shared a filter view "' + save_name + '"'
            msg_data = json.dumps({"view_id": view_id, "save_id": sys_widgets_users_id})
        share_users = list(dict.fromkeys(share_users))
        for usr in share_users:
            if usr:
                notifyps.upd_vals.set({
                    "noti_type": widget_type,
                    "item_id": sys_widgets_users_id,
                    "view_id": view_id,
                    "table_id": 0,
                    "notes_id": 0,
                    "to_user_id": usr,
                    "title": title,
                    "message": message,
                    "msg_data": msg_data
                })
                insertUpdateNotification(notifyps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "User Widget Shared Successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", userps.user_id.get(), "shareUserWidget", str(e))
        raiseAPIError(str(e), 500)

# api/v1/widget/saveuser?dashboard_id=1&sys_widget_id=1&x=0&y=0&c_width=0&c_height=0&htm_flow=0&bg_color=#ffffff&widget_label=Test Widget&widget_setting=&flag=ADD
def saveUserWidget(request: Request):
    print("saveUserWidget -->")
    try:
        params = RequestData.params(request)
        flag = params.get("flag", "")
        dashboard_id = params.get("dashboard_id", 0)
        widget_ref_id = params.get("widget_ref_id", 0)
        widget_label = params.get("widget_label", "")
        widget_setting = normalizeJson(params.get("widget_setting", {}))
        dps.dashboard_id.set(dashboard_id)
        dash_data = getDashboardData(dps)
        widget_list = getattr(dash_data, "widget_list", None)
        # Ensure list
        if not isinstance(widget_list, list):
            widget_list = []
        message = ""
        # ---------------------------------------------------------
        # ADD WIDGET
        # ---------------------------------------------------------
        if flag == "add_widget":
            widget_ref_id = generateRandomString(10, 1)
            widget = {
                "widget_ref_id": widget_ref_id,
                "sys_widget_id": params.get("sys_widget_id", 0),
                "x": params.get("x", 0),
                "y": params.get("y", 0),
                "c_width": params.get("c_width", 0),
                "c_height": params.get("c_height", 0),
                "htm_flow": params.get("htm_flow", 0),
                "bg_color": params.get("bg_color", "#ffffff"),
                "widget_label": widget_label,
                "widget_setting": widget_setting
            }
            # Insert at first position
            widget_list.insert(0, widget)
            message = f"{widget_label} added successfully"
        # ---------------------------------------------------------
        # EDIT WIDGET
        # ---------------------------------------------------------
        elif flag == "edit_widget" and widget_ref_id not in (None, "", 0):
            updates = {
                "widget_label": widget_label,
                "widget_setting": widget_setting,
                "bg_color": params.get("bg_color", "#ffffff"),
                "htm_flow": params.get("htm_flow", 0)
            }
            updateListJsonVal(widget_list, "widget_ref_id", widget_ref_id, updates)
            message = f"{widget_label} updated successfully"
        # ---------------------------------------------------------
        # REMOVE WIDGET
        # ---------------------------------------------------------
        elif flag == "remove_widget" and widget_ref_id not in (None, "", 0):
            removeListJsonVal(widget_list, "widget_ref_id", widget_ref_id)
            message = f"{widget_label} removed successfully"
        # ---------------------------------------------------------
        # SAVE
        # ---------------------------------------------------------
        dps.db_upd_vals.set({"widget_list": widget_list})
        insertUpdateDashboard(dps)
        return JSONResponse(
            status_code=200,
            content={
                "status": True,
                "message": message
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", userps.user_id.get(), "saveUserWidget", str(e))
        raiseAPIError(str(e), 500)

def saveUserWidgetLayout(request: Request):
    print("saveUserWidgetLayout --> ")
    try:
        params = RequestData.params(request)
        dps.dashboard_id.set(params.get("dashboard_id", 0))
        layout_json = normalizeJson(params.get("layout_json"), [])
        # Make sure layout_json is a list
        if not isinstance(layout_json, list):
            layout_json = []
        dash_data = getDashboardData(dps)
        widget_list = getattr(dash_data, "widget_list", [])
        if not isinstance(widget_list, list):
            widget_list = []
        for wdgt in layout_json:
            if not isinstance(wdgt, dict):
                continue
            updates = {
                "x": wdgt.get("x", 0),
                "y": wdgt.get("y", 0),
                "c_width": wdgt.get("c_width", 0),
                "c_height": wdgt.get("c_height", 0)
            }
            updated = updateListJsonVal(widget_list, "widget_ref_id", wdgt.get("widget_ref_id"), updates)
        dps.db_upd_vals.set({"widget_list": widget_list})
        insertUpdateDashboard(dps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Widget Layout saved successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", dps.dashboard_id.get(), "saveUserWidgetLayout", str(e))
        raiseAPIError(str(e), 500)

def copyMoveWidget(request: Request):
    print("copyMoveWidget --> ")
    try:
        params = RequestData.params(request)
        from_dashboard = params.get("from_dashboard", 0)
        to_dashboard = params.get("to_dashboard", 0)
        widget_ref_id = params.get("widget_ref_id", 0)
        flag = params.get("flag", "")
        # Get From Dashboard Widget List
        dps.dashboard_id.set(from_dashboard)
        from_dash = getDashboardData(dps)
        from_widget_list = getattr(from_dash, "widget_list", [])
        if not isinstance(from_widget_list, list):
            from_widget_list = []
        # Get To Dashboard Widget List
        dps.dashboard_id.set(to_dashboard)
        to_dash = getDashboardData(dps)
        to_widget_list = getattr(to_dash, "widget_list", [])
        if not isinstance(to_widget_list, list):
            to_widget_list = []
        # Get Widget from From Dashboard by widget_ref_id
        widget = getListJsonVal(from_widget_list, "widget_ref_id", widget_ref_id)
        if not isinstance(widget, dict):
            widget = {}
        widgetps.sys_widget_id.set(widget.get("sys_widget_id", 0))
        widgetps.fetch_single.set(1)
        widget_data = getWidgetData(widgetps)
        if getattr(widget_data, "is_multiple", 0) in (None, 0, "0") and any(str(item.get("sys_widget_id", 0)) == str(widget.get("sys_widget_id", 0)) for item in to_widget_list):
            return raiseInvalidError("Already Widget is exists")
        # Widget Add to To Dashboard
        to_widget_list.insert(0, {
            "widget_ref_id": generateRandomString(10, 1),
            "sys_widget_id": widget.get("sys_widget_id", 0),
            "x": widget.get("x", 0),
            "y": widget.get("y", 0),
            "c_width": widget.get("c_width", 0),
            "c_height": widget.get("c_height", 0),
            "htm_flow": widget.get("htm_flow", 0),
            "bg_color": widget.get("bg_color", "#ffffff"),
            "widget_label": widget.get("widget_label", ""),
            "widget_setting": widget.get("widget_setting", ""),
        })
        message = widget.get("widget_label", "") + " copied successfully!!"
        dps.dashboard_id.set(to_dashboard)
        dps.db_upd_vals.set({"widget_list": to_widget_list})
        insertUpdateDashboard(dps)
        # Widget Remove from From Dashboard if flag is move
        if flag.upper() == "MOVE":
            message = widget.get("widget_label", "") + " moved successfully!!"
            removeListJsonVal(from_widget_list, "widget_ref_id", widget_ref_id)
            dps.dashboard_id.set(from_dashboard)
            dps.db_upd_vals.set({"widget_list": from_widget_list})
            insertUpdateDashboard(dps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": message
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", userps.user_id.get(), "copyMoveWidget", str(e))
        raiseAPIError(str(e), 500)

def saveViewWidget(request: Request):
    print("saveViewWidget --> ")
    try:
        params = RequestData.params(request)
        view_id = params.get("view_id", 0)
        save_id = params.get("save_id", 0)
        dashboard_id = params.get("dashboard_id", 0)
        widget_type = params.get("widget_type", None)
        x = params.get("x", 0)
        y = params.get("y", 0)
        c_width = params.get("c_width", 3)
        c_height = params.get("c_height", 1.5)
        htm_flow = params.get("htm_flow", 0)
        bg_color = params.get("bg_color", "#ffffff")
        widget_label = params.get("widget_label", "")
        widget_setting = params.get("widget_setting", {})
        pgno = params.get("pgno", 1)
        widget_json = json.dumps({"view_id": view_id, "save_id": save_id, "pgno": pgno})
        widgetps.widget_json.set(widget_json)
        widgetps.widget_type.set(widget_type)
        widgetps.view_id.set(view_id)
        widgetps.fetch_single.set(1)
        widget = getWidgetData(widgetps)
        if widget and widget is not None:
            sys_widget_id = widget.get("sys_widget_id", 0)
        else:
            widgetps.sys_widget_cat_id.set(2)
            widgetps.widget_type.set(widget_type)
            widgetps.widget_icon.set("widget_viewlst.png")
            widgetps.widget_title.set(widget_label)
            widgetps.widget_json.set(widget_json)
            widgetps.view_id.set(view_id)
            widgetps.is_multiple.set(0)
            widgetps.is_system.set(0)
            widgetps.is_global.set(0)
            sys_widget_id = insertUpdateWidget(widgetps)
        # save Widget to User Widget Table
        widgetps.sys_widget_id.set(sys_widget_id)
        dps.dashboard_id.set(dashboard_id)
        dash_data = getDashboardData(dps)
        widget_list = getattr(dash_data, "widget_list", [])
        if isinstance(widget_list, str):
            widget_list = eval(widget_list)
        if not isinstance(widget_list, list):
            widget_list = []
        updates = {
            "widget_setting": widgetps.widget_setting.get()
        }
        updated = updateListJsonVal(widget_list, "sys_widget_id", widgetps.sys_widget_id.get(), updates)
        if not updated:
            widget_list.append({
                "widget_ref_id": generateRandomString(10, 1),
                "sys_widget_id": widgetps.sys_widget_id.get(),
                "x": x,
                "y": y,
                "c_width": c_width,
                "c_height": c_height,
                "htm_flow": htm_flow,
                "bg_color": bg_color,
                "widget_label": widget_label,
                "widget_setting": widget_setting
            })
        dps.db_upd_vals.set({"widget_list": widget_list})
        insertUpdateDashboard(dps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Widget added successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", userps.user_id.get(), "saveViewWidget", str(e))
        raiseAPIError(str(e), 500)

def getBOMXML(request: Request):
    print("getBOMXML --> ")
    try:
        params = RequestData.params(request)
        xmlurl = params.get("xmlurl", "")
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            "Accept": "application/xml,text/xml,text/plain,*/*",
            "Accept-Language": "en-AU,en;q=0.9",
            "Referer": "https://www.bom.gov.au/",
            "Cache-Control": "no-cache",
        }
        response = requests.get(xmlurl, headers=headers, timeout=None, allow_redirects=True)
        xmldata = ""
        error_message = ""
        if response.ok and response.content:
            xmldata = response.text
            error_message = "XML data found."
        elif response.status_code == 403:
            error_message = "Access denied by BOM (HTTP 403). Automated access is blocked."
        else:
            error_message = f"No XML data found. HTTP Status: {response.status_code}"
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": error_message,
                "xmldata": xmldata
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", userps.user_id.get(), "getBOMXML", str(e))
        raiseAPIError(str(e), 500)