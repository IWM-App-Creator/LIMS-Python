from contextvars import ContextVar

class ActionsProperties:
    def __init__(self):
        self.action_id = ContextVar("action_id", default = None)
        self.action_name = ContextVar("action_name", default = None)
        self.action_type = ContextVar("action_type", default = None)
        self.action_icon = ContextVar("action_icon", default = None)
        self.action_color = ContextVar("action_color", default = None)
        self.file_name = ContextVar("file_name", default = None)
        self.function_name = ContextVar("function_name", default = None)
        self.input_variable = ContextVar("input_variable", default = None)
        self.action_json = ContextVar("action_json", default = None)
        self.edit_act_json = ContextVar("edit_act_json", default = None)
        self.yn_global = ContextVar("yn_global", default = None)
        self.short_desc = ContextVar("short_desc", default = None)
        self.preview_img = ContextVar("preview_img", default = None)

        self.view_id = ContextVar("view_id", default = None)
        self.search_text = ContextVar("search_text", default = "")
        self.pg_no = ContextVar("pg_no", default = 1)
        self.record_cnt = ContextVar("record_cnt", default = 0)

        # action_id, action_name, action_type, action_icon, action_color, file_name, function_name, input_variable, action_json, edit_act_json, is_single, is_muliple, yn_global, short_desc, preview_img, status_1, is_delete, created_by, created_date
actionsps = ActionsProperties()