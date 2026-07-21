from contextvars import ContextVar

class CustomViewProperties:
    def __init__(self):
        # custom_view_id, view_name, view_url, dync_cat_id, short_desc, preview_img, status_1, is_delete, created_by, is_metadata, created_date
        self.custom_view_id = ContextVar("custom_view_id", default = 0)
        self.view_name = ContextVar("view_name", default = "")
        self.view_url = ContextVar("view_url", default = "")
        self.dync_cat_id = ContextVar("dync_cat_id", default = "")
        self.short_desc = ContextVar("short_desc", default = "")
        self.preview_img = ContextVar("preview_img", default = "")
        self.status_1 = ContextVar("status_1", default = "")
        self.is_delete = ContextVar("is_delete", default = "")
        self.created_by = ContextVar("created_by", default = "")
        self.created_date = ContextVar("created_date", default = "")

        self.schema_name = ContextVar("schema_name", default = "")
        self.fetch_single = ContextVar("fetch_single", default = 0)
        self.order_by = ContextVar("order_by", default = None)
        self.order_type = ContextVar("order_type", default = None)

customvwps = CustomViewProperties()