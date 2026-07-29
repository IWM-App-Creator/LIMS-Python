from contextvars import ContextVar

class ActivitiesProperties:
    def __init__(self):
        self.log_id = ContextVar("log_id", default = 0)
        self.logtype = ContextVar("logtype", default = "")
        self.data_id = ContextVar("data_id", default = 0)
        self.table_id = ContextVar("table_id", default = 0)
        self.col_id = ContextVar("col_id", default = 0)
        self.item_id = ContextVar("item_id", default = 0)
        self.old_value = ContextVar("old_value", default = 0)
        self.new_value = ContextVar("new_value", default = 0)
        self.desc = ContextVar("desc", default = 0)
        self.is_notify = ContextVar("is_notify", default = 0)
        self.updated_by = ContextVar("updated_by", default = 0)
        self.updated_date = ContextVar("updated_date", default = None)

        self.viewflag = ContextVar("viewflag", default = None)
        self.tableids = ContextVar("tableids", default = None)
        # log_id, logtype, data_id, table_id, col_id, item_id, old_value, new_value, desc, is_notify, status_1, is_delete, updated_by, is_metadata, updated_date
activitiesps = ActivitiesProperties()