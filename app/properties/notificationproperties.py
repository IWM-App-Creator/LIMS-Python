from contextvars import ContextVar

class NotificationProperties:
    def __init__(self):
        self.notificaitons_id = ContextVar("notificaitons_id", default = 0)
        self.noti_type = ContextVar("noti_type", default = "")
        self.item_id = ContextVar("item_id", default = 0)
        self.view_id = ContextVar("view_id", default = 0)
        self.table_id = ContextVar("table_id", default = 0)
        self.notes_id = ContextVar("notes_id", default = 0)
        self.to_user_id = ContextVar("to_user_id", default = 0)
        self.title = ContextVar("title", default = "")
        self.message = ContextVar("message", default = "")
        self.msg_data = ContextVar("msg_data", default = "")
        self.is_read = ContextVar("is_read", default = 0)
        self.read_date = ContextVar("read_date", default = "")
        self.is_new = ContextVar("is_new", default = 0)
        self.is_archive = ContextVar("is_archive", default = 0)
        self.created_by = ContextVar("created_by", default = 0)
        self.total_unread = ContextVar("total_unread", default = 0)
        self.flag = ContextVar("flag", default = 0)        

        self.to_email = ContextVar("to_email", default = "")
        self.subject = ContextVar("subject", default = "")
        self.body = ContextVar("body", default = "")
        self.html = ContextVar("html", default = "")
        self.cc = ContextVar("cc", default = "")
        self.bcc = ContextVar("bcc", default = "")
        self.attachments = ContextVar("attachments", default = [])

notifyps = NotificationProperties()