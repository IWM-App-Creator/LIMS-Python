import json
from app.utils.common import Request, RequestData, raiseAPIError, JSONResponse, userps
from app.helper.generalfunctions import getSelectedUsers, generateRandomString, updateListJsonVal, removeListJsonVal
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
        widget_list = getWidgets(widgetps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Widget List",
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
        if isinstance(share_users, str):
            share_users = share_users.split(",")
        if not isinstance(share_users, list):
            share_users = []
        if widget_type == "ShareWidget":
            title = from_user + " shared a widget with you."
        elif widget_type == "ShareMenu":
            title = save_name
            message = from_user + ' shared a menu "'  + save_name + '"'
            msg_data = json.dumps({"m_center_id": sys_widgets_users_id})
        elif widget_type == "ShareFilter":
            title = save_name
            message = from_user + ' shared a filter view "' + save_name + '"'
            msg_data = json.dumps({"view_id": view_id, "save_id": sys_widgets_users_id})
            share_users = getSelectedUsers(share_users, view_id)
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
    print("saveUserWidget --> ")
    try:
        params = RequestData.params(request)
        # Set Params to Widget Properties
        widgetps.id.set(params.get("id", 0))
        widgetps.dashboard_id.set(params.get("dashboard_id", 0))
        widgetps.sys_widget_id.set(params.get("sys_widget_id", 0))
        widgetps.x.set(params.get("x", 0))
        widgetps.y.set(params.get("y", 0))
        widgetps.c_width.set(params.get("c_width", 0))
        widgetps.c_height.set(params.get("c_height", 0))
        widgetps.htm_flow.set(params.get("htm_flow", 0))
        widgetps.bg_color.set(params.get("bg_color", "#ffffff"))
        widgetps.widget_label.set(params.get("widget_label", ""))
        widgetps.widget_setting.set(params.get("widget_setting", {}))
        widgetps.flag.set(params.get("flag", ""))
        # Get Dashboard Data
        dps.dashboard_id.set(widgetps.dashboard_id.get())
        dash_data = getDashboardData(dps)
        widget_list = getattr(dash_data, "widget_list", [])
        message = ""
        if widgetps.flag.get() == "add_widget":
            widgetps.id.set(generateRandomString(10, 1))
            if widget_list in (None, "", []):
                widget_list = []
            widget_list.append({
                "id": widgetps.id.get(),
                "sys_widget_id": widgetps.sys_widget_id.get(),
                "x": widgetps.x.get(),
                "y": widgetps.y.get(),
                "c_width": widgetps.c_width.get(),
                "c_height": widgetps.c_height.get(),
                "htm_flow": widgetps.htm_flow.get(),
                "bg_color": widgetps.bg_color.get(),
                "widget_label": widgetps.widget_label.get(),
                "widget_setting": widgetps.widget_setting.get()
            })
            message = widgetps.widget_label.get() + " added successfully"
        elif widgetps.flag.get() == "edit_widget" and widgetps.id.get() not in (None, "", 0):
            updates = {
                "widget_label": widgetps.widget_label.get(),
                "widget_setting": widgetps.widget_setting.get(),
                "bg_color": widgetps.bg_color.get(),
                "htm_flow": widgetps.htm_flow.get()
            }
            updated = updateListJsonVal(widget_list, "id", widgetps.id.get(), updates)
            message = widgetps.widget_label.get() + " updated successfully"
        elif widgetps.flag.get() == "remove_widget" and widgetps.id.get() not in (None, "", 0):
            updated = removeListJsonVal(widget_list, "id", widgetps.id.get())
            message = widgetps.widget_label.get() + " removed successfully"
        dps.db_upd_vals.set({"widget_list": widget_list})
        insertUpdateDashboard(dps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": message
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Widget", userps.user_id.get(), "saveUserWidget", str(e))
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
                "id": generateRandomString(10, 1),
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