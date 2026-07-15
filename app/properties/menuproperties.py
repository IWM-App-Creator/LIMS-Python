from contextvars import ContextVar

class MenuProperties:
    def __init__(self):

        # m_centre_id, centre_name, ref_m_c_id, short_desc, preview_img, dync_cat_id, is_public, is_active, is_delete, created_by, is_metadata, created_date
        self.m_centre_id = ContextVar("m_centre_id", default = "")
        self.m_centre_ids = ContextVar("m_centre_ids", default = [])

        self.is_public = ContextVar("is_public", default = "")
        self.is_active = ContextVar("is_active", default = "")
        self.created_by = ContextVar("created_by", default = "")
        self.usr_flag = ContextVar("usr_flag", default = "")
        
        self.fetch_single = ContextVar("fetch_single", default = 0)

        self.menu_array = ContextVar("menu_array", default = [])
        self.menus_output = ContextVar("menus_output", default = [])

        self.menu_id = ContextVar("menu_id", default = "")
        self.parent_menu_id = ContextVar("parent_menu_id", default = "")
        self.m_type = ContextVar("m_type", default = 1)
        self.view_id = ContextVar("view_id", default = 0)
        self.menu_name = ContextVar("menu_name", default = "")
        self.menu_icon = ContextVar("menu_icon", default = "")
        self.menu_color = ContextVar("menu_color", default = "")
        self.menu_url = ContextVar("menu_url", default = "")
        self.is_new_tab = ContextVar("is_new_tab", default = 0)
        self.is_custom_centre = ContextVar("is_custom_centre", default = 0)
        self.add_custom_view = ContextVar("add_custom_view", default = 0)
        self.rank = ContextVar("rank", default = 0)
        self.is_section = ContextVar("is_section", default = "")
        self.callfrom = ContextVar("callfrom", default = "")
        self.is_delete = ContextVar("is_delete", default = None)
        self.created_date = ContextVar("created_date", default = None)
        self.order_by = ContextVar("order_by", default = None)
        self.order_type = ContextVar("order_type", default = None)

        self.last_menu_rank = ContextVar("last_menu_rank", default = 0)
        self.menu_cntr_data = ContextVar("menu_cntr_data", default = {})
        self.menu_centre = ContextVar("menu_centre", default = [])

menups = MenuProperties()