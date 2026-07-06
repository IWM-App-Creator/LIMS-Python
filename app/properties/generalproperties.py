from contextvars import ContextVar

class GeneralProperties:
    def __init__(self):
        self.itmjson = ContextVar("itmjson", default={})
        self.jsonkey = ContextVar("jsonkey", default="")
        self.jsonval = ContextVar("jsonval", default="")
        self.operation = ContextVar("operation", default="")
        self.matchkey = ContextVar("matchkey", default="")
        self.matchvalue = ContextVar("matchvalue", default="")

userps = GeneralProperties()