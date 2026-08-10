from app.utils.common import userps
from app.helper.associationhelper import getViewIdByAssociation
from app.dbfunctions.widgetfunctions import getWidgetsDB
from app.dbfunctions.dashboardfunctions import getDashboardData
from app.properties.associationproperties import associationps
from app.properties.dashboardproperties import dps

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
    print("widget_list --> ", widget_list)
    userwidget_list = []
    for wdgt in usrwdgtarr:
        row = {
            
        }
        userwidget_list.append(row)
    return userwidget_list
