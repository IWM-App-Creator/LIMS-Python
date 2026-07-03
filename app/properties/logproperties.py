class LogProperties:
    def __init__(self):
        self.user_id = 0
        self.first_name = ""
        self.last_name = ""
        self.user_array = []
        self.user_json = {}

logps = LogProperties()


class LogProperties:
    def __init__(self):
        self.srno = 0

logps = LogProperties()

from contextvars import ContextVar
class LogProperties:
    def __init__(self):
        self.srno = ContextVar("srno", default = "")

logps = LogProperties()
