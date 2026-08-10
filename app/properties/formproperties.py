from contextvars import ContextVar

class FormProperties:
    def __init__(self):
        self.form_id = ContextVar("form_id", default = 0)
        self.form_name = ContextVar("form_name", default = "")
        self.form_meta = ContextVar("form_meta", default = {})
        self.form_cols = ContextVar("form_cols", default = [])
        self.output_type = ContextVar("output_type", default = {})


        # form_id, form_name, form_meta, form_cols, output_type, dync_cat_id, is_delete, created_by, is_metadata, created_date

formps = FormProperties()