from app.utils.common import userps
from app.helper.associationhelper import getViewIdByAssociation
from app.dbfunctions.widgetfunctions import getWidgetsDB, getUserWidgetsDB
from app.properties.associationproperties import associationps

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
        if not is_admin and getattr(widget, "widget_type", "") == "VIEWWIDGET":
            is_valid = 0
            for view_id in view_ids:
                if getattr(widget, "view_id", 0) == view_id:
                    is_valid = 1
        if is_valid == 1:
            row = {
                "sys_widget_id": getattr(widget, "sys_widget_id", 0),
                "widget_title": getattr(widget, "widget_title", ""),
                "widget_json": getattr(widget, "widget_json", ""),
                "widget_type": getattr(widget, "widget_type", ""),
                "widget_icon": getattr(widget, "widget_icon", ""),
                "is_visible": getattr(widget, "is_visible", 0),
                "is_global": getattr(widget, "is_global", 0),
                "view_id": getattr(widget, "view_id", 0),
                "view_name": getattr(widget, "view_name", ""),
                "view_url_full": getattr(widget, "url", ""),
                "widget_added": getattr(widget, "widget_added", 0),
            }
            widget_list.append(row)
    return widget_list

def getUserWidgets(widgetps):
    usrwdgtarr = getUserWidgetsDB(widgetps)
    userwidget_list = []
    for wdgt in usrwdgtarr:
        row = {
            "sys_widgets_users_id": getattr(wdgt, "sys_widgets_users_id", 0),
            "sys_widget_id": getattr(wdgt, "sys_widget_id", 0),
            "widget_type": getattr(wdgt, "widget_type", ""),
            "widget_title": getattr(wdgt, "widget_title", ""),
            "widget_json": getattr(wdgt, "widget_json", ""),
            "widget_label": getattr(wdgt, "widget_label", ""),
            "widget_setting": getattr(wdgt, "widget_setting", ""),
            "widget_icon": getattr(wdgt, "widget_icon", ""),
            "c_width": getattr(wdgt, "c_width", 0),
            "c_height": getattr(wdgt, "c_height", 0),
            "htm_flow": getattr(wdgt, "htm_flow", ""),
            "bg_color": getattr(wdgt, "bg_color", ""),
            "view_id": getattr(wdgt, "view_id", 0),
            "view_name": getattr(wdgt, "view_name", ""),
            "view_url_full": getattr(wdgt, "url", ""),
            "outlook_token": int(getattr(wdgt, "TODO", "") == 1),
            "summarydata": getattr(wdgt, "summarydata", ""),
            "summaryhtml": getattr(wdgt, "summaryhtml", ""),
        }
        userwidget_list.append(row)
    return userwidget_list
