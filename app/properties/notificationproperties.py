from contextvars import ContextVar

class NotificationProperties:
    def __init__(self):
        # Global Variables
        self.to_email = ContextVar("to_email", default="")
        self.subject = ContextVar("subject", default="")
        self.body = ContextVar("body", default="")
        self.html = ContextVar("html", default="")
        self.cc = ContextVar("cc", default="")
        self.bcc = ContextVar("bcc", default="")
        self.attachments = ContextVar("attachments", default=[])

notifyps = NotificationProperties()