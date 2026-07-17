from pathlib import Path
from app.utils.common import formatDate, DB, text, nowWithTimeZone, userps
from app.dbfunctions.dbfunctions import createWSDBSchema
from app.dbfunctions.userfunctions import getUserDataByID
from app.dbfunctions.dashboardfunctions import insertUpdateDashboard
from app.helper.generalfunctions import formatUserDisplayName, generateRandomString, uploadFile
import app.dbfunctions.workspacefunctions as wsfnct
import app.properties.dbproperties as dps
import shutil
import time
from fastapi import UploadFile

def getWorkspaceByUser(wsps):
    wsfnct.getWSListByUsers(wsps)
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
    wsps.domain_flag.set(0)
    wsps.fetch_single.set(0)
    wsfnct.getUserWSData(wsps)
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

def createWorkspace(wsps):
    print("createWorkspace --> ")
    # Step 1 : Add To Workspace
    schema_name = generateRandomString(length = 12, hasdigits = 1)
    wsps.schema_name.set(schema_name)
    wsps.ws_logo.set(uploadFile(wsps.ws_url.get(), "", wsps.ws_logo_file.get())) # Upload File Functions Here
    wsfnct.insertUpdateWorkspace(wsps) # Create New Workspace # workspace_id
    # Step 2 : Assign WS to User
    # $user_wp_id = $WSFunctionsController->assignUserToWorkspace($workspace_id, $user_id, $user_id, 1, 0);

    # Step 3 : /* Email User */
    # $u_name = $userdtlarr->first_name . " " . $userdtlarr->last_name;
    # $password = "Your Password";
    # $WSFunctionsController->sendWSInvitationEmail($u_name, $userdtlarr->email, $password, $workspace_id);
    
    # Step 4 : Setup Schema & Create System Tables
    createWSDBSchema(schema_name) # Create Schema & Copy Table
    copyActionData(schema_name) # Copy Action Table Data
    copyWidgetData(schema_name) # Copy Widget Table Data
    copyIntegrationData(schema_name) # Copy Integration Table Data

def copyActionData(new_schema_name: str):
    DB.executeDBStatement(
        text(f"""
            INSERT INTO `{new_schema_name}`.sys_dynamic_actions
            SELECT *
            FROM systemconfig.sys_dynamic_actions
            WHERE yn_global = 1
        """)
    )
    updateCreatedBy(new_schema_name, "sys_dynamic_actions")

def copyWidgetData(new_schema_name: str):
    DB.executeDBStatement(
        text(f"""
            INSERT INTO `{new_schema_name}`.sys_widgets_category
            SELECT *
            FROM systemconfig.sys_widgets_category
        """)
    )
    DB.executeDBStatement(
        text(f"""
            INSERT INTO `{new_schema_name}`.sys_widget_master
            SELECT *
            FROM systemconfig.sys_widget_master
        """)
    )
    updateCreatedBy(new_schema_name, "sys_widgets_category")
    updateCreatedBy(new_schema_name, "sys_widget_master")

    dps.dashboard_name.set("Default")
    dps.is_active.set(1)
    insertUpdateDashboard(dps) # Create Blank Dashboard
    # dashboard_id = dps.dashboard_id.get()
    # assignWidgetToUser(new_schema_name, 1, dashboard_id, user_wp_id, 1)
    # assignWidgetToUser(new_schema_name, 2, dashboard_id, user_wp_id, 2)
    # assignWidgetToUser(new_schema_name, 3, dashboard_id, user_wp_id, 3)

def copyIntegrationData(new_schema_name: str):
    DB.executeDBStatement(
        text(f"""
            INSERT INTO `{new_schema_name}`.sys_integration_cat
            SELECT *
            FROM systemconfig.sys_integration_cat
        """)
    )
    DB.executeDBStatement(
        text(f"""
            INSERT INTO `{new_schema_name}`.sys_integration_master
            SELECT *
            FROM systemconfig.sys_integration_master
        """)
    )
    updateCreatedBy(new_schema_name, "sys_integration_cat")
    updateCreatedBy(new_schema_name, "sys_integration_master")

def updateCreatedBy(schema_name: str, table_name: str):
    DB.executeDBStatement(
        text(f"""
            UPDATE `{schema_name}`.`{table_name}`
            SET
                created_by = :created_by,
                created_date = :created_date
        """),
        {
            "created_by": userps.user_id.get(),
            "created_date": nowWithTimeZone()
        }
    )

def updateWorkspace(wsps):
    wsfnct.getSingleWorkspaceData(wsps) # Get Workspace by ID
    wsdata = wsps.ws_data.get()
    ws_url = ""
    if wsdata :
        ws_url = wsdata.ws_url
    wsps.ws_logo.set(uploadFile(ws_url, "", wsps.ws_logo_file.get())) # Upload File Functions Here
    db_upd_vals = {}
    if wsps.workspace_name.get() not in (None, ""):
        db_upd_vals["workspace_name"] = wsps.workspace_name.get()
    if wsps.size_limit.get() not in (None, ""):
        db_upd_vals["size_limit"] = wsps.size_limit.get()
    if wsps.ws_logo.get() not in (None, ""):
        db_upd_vals["ws_logo"] = wsps.ws_logo.get()
    wsps.db_upd_vals.set(db_upd_vals)
    wsfnct.insertUpdateWorkspace(wsps)

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