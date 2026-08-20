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
    if isinstance(tab_id, (list, tuple)):
        tab_ids = tab_id
    else:
        tab_ids = str(tab_id).split(",")
    tab_ids = [str(tab).strip().replace(".0", "") for tab in tab_ids if str(tab).strip()]
    print("tab_ids --> ", tab_ids)
    # -------------------------------------------------
    # Get existing JSON
    # -------------------------------------------------
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
    # -------------------------------------------------
    # Conditional Color
    # -------------------------------------------------
    if col_flag in ("col_metadata", "col_colors", "action_group_list"):
        if not isinstance(data, dict):
            data = {}
        # key_val can be JSON string or already parsed list
        if isinstance(key_val, str):
            try:
                key_val = json.loads(key_val)
            except json.JSONDecodeError:
                key_val = []
        if not isinstance(key_val, list):
            key_val = []
        # ---------------------------------------------
        # Update one or multiple tabs
        # ---------------------------------------------
        for tab in tab_ids:
            data[f"tab_{tab}"] = key_val
    # -------------------------------------------------
    # USER SETTING
    # -------------------------------------------------
    elif col_flag == "user_setting":
        # ---------------------------------------------
        # Group setting
        # ---------------------------------------------
        if key_flag == "group_tab":
            try:
                key_val = int(key_val)
            except (ValueError, TypeError):
                pass
            data["group_tab"] = key_val
        # ---------------------------------------------
        # Tab setting
        # ---------------------------------------------
        else:
            tabs = data.setdefault("tabs", {})
            key_flags = str(key_flag).split("||")
            key_vals = str(key_val).split("||")
            # -----------------------------------------
            # Apply same values to ALL selected tabs
            # -----------------------------------------
            for tab in tab_ids:
                tab_key = f"tab_{tab}"
                # Existing tab or new tab
                tab_data = tabs.setdefault(tab_key, {})
                for flag, value in zip(key_flags, key_vals):
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        pass
                    tab_data[flag] = value
    # -------------------------------------------------
    # Save
    # -------------------------------------------------
    viewlyps.db_upd_vals.set({col_flag: data})
    print("viewlyps.db_upd_vals.get() --> ", viewlyps.db_upd_vals.get())
    return insertUpdateUserLayout(viewlyps)