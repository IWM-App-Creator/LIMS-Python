import json
from app.utils.common import userps

def setWorkspaceOutput(wsps):
    ws_datas = wsps.ws_data.get()
    ws_data = []
    for ws in ws_datas:
        row = {
            "workspace_id": ws.workspace_id,
            "workspace_name": ws.workspace_name,
            "ws_url": ws.ws_url,
            "schema_name": ws.schema_name,
            "ws_role_id": ws.ws_role_id,
            "is_accepted": ws.is_accepted
        }
        ws_data.append(row)
    wsps.ws_data.set(json.dumps(ws_data))