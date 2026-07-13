from contextvars import ContextVar

class viewlayoutproperties:
    def __init__(self):

        self.view_id = ContextVar("view_id", default = "0")
        self.call_from = ContextVar("call_from", default = "")

viewlyps = viewlayoutproperties()