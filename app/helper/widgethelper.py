from collections import defaultdict
from app.utils.common import userps
from app.helper.associationhelper import getViewIdByAssociation
from app.dbfunctions.widgetfunctions import getWidgetsDB, getWidgetData
from app.dbfunctions.dashboardfunctions import getDashboardData
from app.dbfunctions.viewfunctions import getViewDataByID
from app.properties.associationproperties import associationps
from app.properties.dashboardproperties import dps
from app.properties.viewproperties import viewps

def getWidgets(widgetps):
    is_admin = (userps.ws_role_id.get() == 1 or userps.role_id.get() == 1)
    if not is_admin:
        associationps.user_id.set(userps.user_id.get())
        getViewIdByAssociation(associationps)
        view_ids = associationps.dyncviews.get()
        if not isinstance(view_ids, list):
            view_ids = []
    widgetarr = getWidgetsDB(widgetps)
    widget_list = []
    for widget in widgetarr:
        is_valid = 1
        view_url = ""
        if not is_admin and getattr(widget, "widget_type", "") == "VIEWWIDGET":
            is_valid = 0
            for view_id in view_ids:
                if getattr(widget, "view_id", 0) == view_id:
                    is_valid = 1
        if is_valid == 1:
            if getattr(widget, "url", "") not in (None, ""):
                view_url = getattr(widget, "url", "")
            row = {
                "sys_widget_id": getattr(widget, "sys_widget_id", 0),
                "sys_widget_cat_id": getattr(widget, "sys_widget_cat_id", 0),
                "widget_title": getattr(widget, "widget_title", ""),
                "widget_json": getattr(widget, "widget_json", ""),
                "widget_type": getattr(widget, "widget_type", ""),
                "widget_icon": getattr(widget, "widget_icon", ""),
                "is_visible": getattr(widget, "is_visible", 0),
                "is_global": getattr(widget, "is_global", 0),
                "view_id": getattr(widget, "view_id", 0),
                "view_name": getattr(widget, "view_name", ""),
                "view_url_full": view_url,
                "widget_added": getattr(widget, "widget_added", 0),
            }
            widget_list.append(row)
    return widget_list

def getUserWidgets(widgetps):
    dps.dashboard_id.set(widgetps.dashboard_id.get())
    usrwdgtarr = getDashboardData(dps)
    widget_list = getattr(usrwdgtarr, "widget_list", [])
    if not isinstance(widget_list, list):
        widget_list = [] 
    userwidget_list = []
    sys_widget_ids = list({
        str(wdgt.get("sys_widget_id"))
        for wdgt in widget_list
        if wdgt.get("sys_widget_id") not in (None, "", 0)
    })
    if not sys_widget_ids:
        return []
    widgetps.sys_widget_ids.set(sys_widget_ids)
    widgetps.fetch_single.set(0)
    widget_master_data  = getWidgetData(widgetps)
    widget_master_map = {}
    for wigtm in widget_master_data:
        widget_json = getattr(wigtm, "widget_json", {})
        if viewps.userview.get() not in (None, "", ()) and getattr(wigtm, "widget_type", "") == "VIEWWIDGET" and widget_json not in (None, {}, [], ""):
            if isinstance(widget_json, str):
                widget_json = eval(widget_json)
            view_id = widget_json.get("view_id", 0)
            viewps.view_id.set(view_id)
            getViewDataByID(viewps)
            viewps.view_name.set(getattr(viewps.userview.get(), "view_name", ""))
            viewps.view_url.set(getattr(viewps.userview.get(), "url", ""))
        widgetitm = {
            "sys_widget_id": getattr(wigtm, "sys_widget_id", 0),
            "widget_type": getattr(wigtm, "widget_type", ""),
            "widget_title": getattr(wigtm, "widget_title", ""),
            "widget_json": widget_json,
            "widget_icon": getattr(wigtm, "widget_icon", ""),
            "view_id": viewps.view_id.get() or 0,
            "view_name": viewps.view_name.get() or "",
            "view_url": viewps.view_url.get() or "",
            "outlook_token": int(getattr(wigtm, "widget_type", "") == "TODO")
        }
        widget_master_map[str(getattr(wigtm, "sys_widget_id", 0))] = widgetitm
    for wdgt in widget_list:
        sys_widget_id = str(wdgt.get("sys_widget_id", ""))
        row = {
            "id": wdgt.get("id", 0),
            "sys_widget_id": wdgt.get("sys_widget_id", 0),
            "x": wdgt.get("x", 0),
            "y": wdgt.get("y", 0),
            "c_width": wdgt.get("c_width", 0),
            "c_height": wdgt.get("c_height", 0),
            "htm_flow": wdgt.get("htm_flow", 0),
            "bg_color": wdgt.get("bg_color", "#ffffff"),
            "widget_label": wdgt.get("widget_label", ""),
            "widget_setting": wdgt.get("widget_setting", {}),
        }
        master_data = widget_master_map.get(sys_widget_id)
        if master_data:
            row.update(master_data)
        userwidget_list.append(row)
    return userwidget_list
