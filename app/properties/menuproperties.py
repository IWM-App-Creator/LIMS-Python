from contextvars import ContextVar

class MenuProperties:
    def __init__(self):
        self.m_centre_id = ContextVar("m_centre_id", default=0)
        self.is_public = ContextVar("is_public", default=0)
        self.is_active = ContextVar("is_active", default=0)

        self.usr_flag = ContextVar("usr_flag", default=0)
        

menups = MenuProperties()