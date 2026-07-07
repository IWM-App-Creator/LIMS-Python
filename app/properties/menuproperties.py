from contextvars import ContextVar

class MenuProperties:
    def __init__(self):
        self.m_centre_id = ContextVar("m_centre_id", default = "")
        self.is_public = ContextVar("is_public", default = "")
        self.is_active = ContextVar("is_active", default = "")
        self.created_by = ContextVar("created_by", default = "")
        self.usr_flag = ContextVar("usr_flag", default = "")
        
        self.fetch_single = ContextVar("fetch_single", default = 0)

        self.menu_array = ContextVar("menu_array", default = [])
        self.menus_output = ContextVar("menus_output", default = [])
menups = MenuProperties()