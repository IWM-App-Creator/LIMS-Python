from contextvars import ContextVar

class chatbotproperties:
    def __init__(self):
        # CB Lib Modules Properties
        self.cb_lib_module_id = ContextVar("cb_lib_module_id", default = 0)
        self.module_name = ContextVar("module_name", default = "")
        self.module_icon = ContextVar("module_icon", default = "")
        self.cb_rank = ContextVar("cb_rank", default = 0)

        # CB User Module Properties
        self.cb_user_module_id = ContextVar("cb_user_module_id", default = 0)
        self.rank = ContextVar("rank", default = 0)

        # ChatBot API Properties
        self.view_id = ContextVar("view_id", default = "0")
        self.table_id = ContextVar("table_id", default = "0")
        self.workspace_id = ContextVar("workspace_id", default = "")
        self.integration_id = ContextVar("integration_id", default = "0")
        self.endpoint_id = ContextVar("endpoint_id", default = "0")

        self.session_id = ContextVar("session_id", default = "")
        self.hf_sys_db_ai_id = ContextVar("hf_sys_db_ai_id", default = "")

        self.schema_output = ContextVar("schema_output", default = "")
        self.db_query = ContextVar("db_query", default = "")

        self.query = ContextVar("query", default = "")
        self.type = ContextVar("type", default = "faqs")
        self.subtype = ContextVar("subtype", default = "")

        self.link = ContextVar("link", default = "")
        self.chatbot_view_url = ContextVar("chatbot_view_url", default = "")
        self.chat_history = ContextVar("chat_history", default = "")

        self.strchat_history = ContextVar("strchat_history", default = "")
        self.strcb_buttons = ContextVar("strcb_buttons", default = "")
        self.code = ContextVar("code", default = "")
        self.response = ContextVar("response", default = "")

        self.cb_md_list = ContextVar("cb_md_list", default = [])
        
cbps = chatbotproperties()