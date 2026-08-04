from contextvars import ContextVar

class NotesProperties:
    def __init__(self):
        self.notes_id = ContextVar("notes_id", default = 0)
        self.note_ids = ContextVar("note_ids", default = "")
        self.parent_id = ContextVar("parent_id", default = 0)
        self.view_id = ContextVar("view_id", default = 0)
        self.table_id = ContextVar("table_id", default = 0)
        self.col_id = ContextVar("col_id", default = 0)
        self.item_id = ContextVar("item_id", default = 0)
        self.item_ids = ContextVar("item_ids", default = "")
        self.note = ContextVar("note", default = 0)
        self.note_txt = ContextVar("note_txt", default = 0)
        self.status_1 = ContextVar("status_1", default = 0)
        self.is_delete = ContextVar("is_delete", default = 0)
        self.created_by = ContextVar("created_by", default = 0)
        self.created_date = ContextVar("created_date", default = None)

        self.share_users = ContextVar("share_users", default = [])
        self.reminder_date = ContextVar("reminder_date", default = None)

        self.showdel = ContextVar("showdel", default = 0)
        #notes_id, parent_id, view_id, table_id, col_id, item_id, note, note_txt, status_1, is_delete, created_by, created_date
notesps = NotesProperties()