# from app.utils.common import select, DB, userps, formatDate
from app.dbfunctions.chatbotfunctions import getUserCBMdFromDB, insertUserCBMD

class ChatbotHelper:

    @staticmethod
    def setCBQuesAnsParam(cbps, params):
        cbps.view_id.set(params.get("view_id", "0"))
        cbps.table_id.set(params.get("table_id", "0"))
        cbps.workspace_id.set(params.get("workspace_id", "0"))
        cbps.integration_id.set(params.get("integration_id", "0"))
        cbps.endpoint_id.set(params.get("endpoint_id", "0"))
        cbps.session_id.set(params.get("session_id", ""))
        cbps.hf_sys_db_ai_id.set(params.get("hf_sys_db_ai_id", ""))
        cbps.schema_output.set(params.get("schema_output", ""))
        cbps.db_query.set(params.get("db_query", ""))
        cbps.query.set(params.get("query", ""))
        cbps.type.set(params.get("type", ""))
        cbps.subtype.set(params.get("subtype", ""))
        cbps.link.set(params.get("link", ""))
        cbps.chatbot_view_url.set(params.get("chatbot_view_url", ""))
        cbps.chat_history.set(params.get("chat_history", ""))

    @staticmethod
    def getUserCBModules(cbps):
        cbps.cb_md_list.set([]) # Clean Output Array
        itm_list = []
        cbmdarr = getUserCBMdFromDB()
        # If no modules exist, insert FAQ as default
        if not cbmdarr:
            insertUserCBMD()    
        for cbmd in cbmdarr:
            row = {
                "cb_user_module_id": getattr(cbmd, "cb_user_module_id", "0"),
                "cb_lib_module_id": getattr(cbmd, "cb_lib_module_id", "0"),
                "module_icon": getattr(cbmd, "module_icon", ""),
                "module_name": getattr(cbmd, "module_name", ""),
            }
            itm_list.append(row)
        cbps.cb_md_list.set(itm_list)

cbhlp = ChatbotHelper()