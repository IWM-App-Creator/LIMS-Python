import json
from app.utils.common import select, DB, raiseInvalidError, userps
from app.dbfunctions.dbtablesfunctions import getDBTableData
from app.dbfunctions.viewlayoutfunctions import getViewLayoutDataByID
from app.helper.generalfunctions import sortObjectsByKey
from app.properties.dbproperties import dbps
from app.helper import dbhelper as dbhlp
from app.dbfunctions.viewlayoutfunctions import insertUpdateUserLayout

def setViewLayoutParam(viewps, params):
    viewps.view_id.set(params.get("view_id", ""))
    # viewps.call_from.set(params.get("call_from", "DynamicView"))
    # viewps.tab_id.set(params.get("tab_id", "0"))
    # viewps.page_no.set(params.get("page_no", 1))
    # viewps.search_text.set(params.get("search_text", ""))
    # viewps.filter_qry.set(params.get("filter_qry", ""))

def saveUserLayoutData(viewlyps):
    tab_id = viewlyps.tab_id.get()
    col_flag = viewlyps.col_flag.get()
    key_flag = viewlyps.key_flag.get()
    key_val = viewlyps.key_val.get()
    usr_layout = getViewLayoutDataByID(viewlyps)
    print("usr_layout --> ", usr_layout)
    if usr_layout:
        viewlyps.srno.set(getattr(usr_layout, "srno", 0))
        current_value = getattr(usr_layout, col_flag, None)
        if current_value in (None, ""):
            data = {}
        elif isinstance(current_value, str):
            try:
                data = json.loads(current_value)
            except json.JSONDecodeError:
                data = {}
        else:
            data = current_value
    else:
        data = {}
    if col_flag == "user_setting":
        tabs = data.setdefault("tabs", {})
        tab_key = f"tab_{tab_id}"
        tab_data = tabs.setdefault(tab_key, {})
        try:
            key_val = int(key_val)
        except (ValueError, TypeError):
            pass
        tab_data[key_flag] = key_val
    viewlyps.db_upd_vals.set({col_flag: json.dumps(data)})
    insertUpdateUserLayout(viewlyps)