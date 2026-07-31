from contextvars import ContextVar

class WidgetProperties:
    def __init__(self):
        self.sys_widget_id = ContextVar("sys_widget_id", default = None)
        self.sys_widget_cat_id = ContextVar("sys_widget_cat_id", default = None)
        self.widget_type = ContextVar("widget_type", default = None)
        self.widget_icon = ContextVar("widget_icon", default = None)
        self.widget_title = ContextVar("widget_title", default = None)
        self.widget_dtl = ContextVar("widget_dtl", default = None)
        self.widget_json = ContextVar("widget_json", default = None)
        self.view_id = ContextVar("view_id", default = None)
        self.is_visible = ContextVar("is_visible", default = None)
        self.is_multiple = ContextVar("is_multiple", default = None)
        self.is_system = ContextVar("is_system", default = None)
        self.is_global = ContextVar("is_global", default = None)
        self.is_delete = ContextVar("is_delete", default = None)
        self.created_by = ContextVar("created_by", default = None)
        self.created_date = ContextVar("created_date", default = None)

        self.dashboard_id = ContextVar("dashboard_id", default = None)
        self.search_text = ContextVar("search_text", default = None)
        self.preview = ContextVar("preview", default = None)


        self.fetch_single = ContextVar("preview", default = None)

        # sys_widget_id, sys_widget_cat_id, widget_type, widget_icon, widget_title, widget_dtl, widget_json, view_id, is_visible, is_multiple, is_system, is_global, is_delete, created_by, created_date

        # sys_widgets_users_id, sys_widget_id, dashboard_id, user_id, c_width, c_height, htm_flow, bg_color, widget_label, widget_setting, rank, status_1, is_delete, created_by, created_date
widgetps = WidgetProperties()