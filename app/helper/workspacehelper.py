from pathlib import Path
from app.utils.common import formatDate
from app.dbfunctions.userfunctions import getUserDataByID
from app.helper.generalfunctions import formatUserDisplayName

def setWorkspaceOutput(wsps):
    ws_datas = wsps.ws_data.get()
    ws_data = []
    for ws in ws_datas:
        # print(dict(ws._mapping))
        wsps.ws_url.set(ws.ws_url)
        getWSFilesCountAndSize(wsps)
        used_size = wsps.used_size.get()
        usages = (used_size * 100 ) / ws.size_limit
        created_name = "";
        user = getUserDataByID(ws.created_by)

        total_users = int(getattr(ws, "ownercnt", 0)) + int(getattr(ws, "usercnt", 0)) + int(getattr(ws, "noaccesscnt", 0))
        if user:
            first_name = getattr(user, "first_name", "")
            last_name = getattr(user, "last_name", "")
            created_name = formatUserDisplayName(first_name = first_name, last_name = last_name)
        row = {
            "workspace_id": ws.workspace_id,
            "ws_role_id": ws.ws_role_id,
            "workspace_name": ws.workspace_name,
            "ws_url": ws.ws_url,
            "schema_name": ws.schema_name,
            "ws_logo": ws.ws_logo,
            "ai_priority": ws.ai_priority,
            "is_setup": ws.is_setup,
            "size_limit": ws.size_limit,
            "files": wsps.file_count.get(),
            "size": f"{used_size:.2f} MB",
            "usages": f"{usages:.2f} %",
            "total_users": total_users,
            "owner_users": int(getattr(ws, "ownercnt", 0)),
            "only_users": int(getattr(ws, "usercnt", 0)),
            "no_access": int(getattr(ws, "noaccesscnt", 0)),
            "created_by": ws.created_by,
            "created_name": created_name,
            "created_date": formatDate(from_date = ws.created_date)
        }
        ws_data.append(row)
    wsps.ws_data.set(ws_data)

def getUserWSList(wsps):
    # wsps.domain_flag.set(0)
    # wsps.fetch_single.set(0)
    # getUserWSData(wsps)
    ws_datas = wsps.ws_data.get()
    ws_data = []
    for ws in ws_datas:
        row = {
            "workspace_id": getattr(ws, "workspace_id", 0),
            "workspace_name": getattr(ws, "workspace_name", ""),
            "ws_url": getattr(ws, "ws_url", ""),
            "schema_name": getattr(ws, "schema_name", ""),
            "ws_role_id": getattr(ws, "ws_role_id", 2),
            "is_accepted": getattr(ws, "is_accepted", 0),
        }
        ws_data.append(row)
    wsps.ws_data.set(ws_data)

def getWSCommonFolderArray():
    WS_COMMON_FOLDERS = [
        "action",
        "barcode",
        "catalogunit",
        "csv",
        "dbtblcsv",
        "dyncview",
        "integration",
        "methodology",
        "openai",
        "pdf",
        "projects",
        "tinymce",
        "users",
        "view"
    ]
    return WS_COMMON_FOLDERS

def getWSFilesCountAndSize(wsps):
    ws_url = wsps.ws_url.get()
    # ws_url
    file_count = 0
    total_size = 0
    ws_path = Path("wsassets/uploads") / ws_url
    for folder in getWSCommonFolderArray():
        folder_path = ws_path / folder
        if not folder_path.exists():
            continue
        for file in folder_path.rglob("*"):
            if file.is_file():
                file_count += 1
                total_size += file.stat().st_size
    used_size = total_size / (1024 * 1024)
    wsps.ws_url.set(file_count)
    wsps.used_size.set(used_size)