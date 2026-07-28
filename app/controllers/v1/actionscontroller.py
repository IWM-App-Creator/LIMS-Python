from app.utils.common import Request, RequestData, JSONResponse
from app.properties.actionsproperties import actionsps
from app.dbfunctions.actionsfunctions import getActionList

def getActions(request: Request):
    print("getActions --> ")
    # set Params to Properties
    params = RequestData.params(request)
    actionsps.view_id.set(params.get("view_id", 0))
    actionsps.search_text.set(params.get("search_text", ""))
    actionsps.action_type.set(params.get("action_type", ""))
    actionsps.pg_no.set(params.get("pg_no", 1))
    actionarr = getActionList(actionsps)
    action_list = []
    for action in actionarr:
        row = {
            "action_id": action.action_id,
            "action_name": action.action_name,
            "action_type": action.action_type,
            "action_icon": action.action_icon,
            "action_color": action.action_color,
            "file_name": action.file_name,
            "function_name": action.function_name,
            "input_variable": action.input_variable,
            "action_json": action.action_json,
            "edit_act_json": action.edit_act_json,
            "short_desc": action.short_desc,
            "preview_img": action.preview_img
        }
        action_list.append(row)
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "Action List Data",
            "action_list": action_list,
            "total_records": actionsps.record_cnt.get()
        }
    )