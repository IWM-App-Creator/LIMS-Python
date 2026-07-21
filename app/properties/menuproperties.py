from contextvars import ContextVar

class MenuProperties:
    def __init__(self):
        # Menu Centre Params
        self.m_centre_id = ContextVar("m_centre_id", default = "")
        self.m_centre_ids = ContextVar("m_centre_ids", default = "")
        self.centre_name = ContextVar("centre_name", default = "")
        self.menu_json = ContextVar("menu_json", default = {})
        self.short_desc = ContextVar("short_desc", default = "")
        self.preview_img = ContextVar("preview_img", default = "")
        self.is_public = ContextVar("m_centre_id", default = "")
        self.is_active = ContextVar("m_centre_id", default = "")
        self.created_by = ContextVar("created_by", default = 0)

        # Menu Json Params
        self.menu_id = ContextVar("menu_id", default = "")
        self.menu_name = ContextVar("menu_name", default = "")
        self.menu_url = ContextVar("menu_url", default = "")
        self.menu_icon = ContextVar("menu_icon", default = "")
        self.menu_color = ContextVar("menu_color", default = "")
        self.m_type = ContextVar("m_type", default = 1)
        self.item_id = ContextVar("item_id", default = 0)
        self.is_new_tab = ContextVar("is_new_tab", default = 0)
        self.is_section = ContextVar("is_section", default = 0)
        self.submenu = ContextVar("submenu", default = [])

        self.schema_name = ContextVar("schema_name", default = "")
        self.menu_cntr_data = ContextVar("menu_cntr_data", default = {})

menups = MenuProperties()