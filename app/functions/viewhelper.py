import json
from app.utils.common import select, DB, userps
from app.dbfunctions.dbtablesfunctions import getDBTableData
from app.properties.dbproperties import dbps

def processViewInputParam(viewps, params):
    viewps.view_id.set(params.get("view_id", ""))
    viewps.call_from.set(params.get("call_from", "DynamicView"))
    viewps.tab_id.set(params.get("tab_id", ""))
    viewps.page_no.set(params.get("page_no", ""))
    viewps.txtsearch.set(params.get("txtsearch", ""))
    viewps.filterqry.set(params.get("filterqry", ""))

def setViewDataProperties(viewps):
    userview = viewps.userview.get()
    viewps.view_id.set(userview.view_id)
    viewps.view_name.set(userview.view_name)
    viewps.view_url.set(userview.url)
    viewps.view_type.set(userview.view_type)
    viewps.view_options.set(userview.view_options)
    viewps.view_cols.set(userview.view_cols)
    viewps.view_joins.set(userview.view_joins)
    viewps.view_child.set(userview.view_child)
    viewps.view_actions.set(userview.view_actions)
    parseViewOptions(viewps)

def parseViewOptions(viewps):
    viewopt = viewps.view_options.get() or {}
    viewps.table_id.set(viewopt.get("table_id", 0))
    viewps.table_name.set(viewopt.get("table_name", ""))
    viewps.view_qry.set(viewopt.get("view_qry", ""))
    viewps.primary_col.set(viewopt.get("primary_col", ""))
    viewps.primary_colnm.set(viewopt.get("primary_colnm", ""))    
    viewps.delete_col.set(viewopt.get("delete_col", ""))
    viewps.show_deleted.set(viewopt.get("show_deleted", 0))
    viewps.enable_newline.set(viewopt.get("enable_newline", 0))
    viewps.enable_join_save.set(viewopt.get("enable_join_save", 0))
    viewps.is_child_view.set(viewopt.get("is_child_view", 0))
    viewps.enable_child_srch.set(viewopt.get("enable_child_srch", 0))
    viewps.enable_chart.set(viewopt.get("enable_chart", 0))

def setViewTableCols(viewps):
    # Get View Columns
    view_cols = viewps.view_cols.get()
    view_cols = view_cols.get("view_cols", [])
    col_id_arr = []
    for col in view_cols:
        col_id_arr.append(col["col_id"])
    col_id_arr = list(dict.fromkeys(col_id_arr))
    # Get Table Col
    dbps.col_ids.set(col_id_arr)
    dbps.is_del_tbl.set(0)
    dbps.is_del_col.set(0)
    tblcol = getDBTableData(dbps)
    tbl_cols = []
    for col in tblcol:
        col_options = (col.col_options or {}).copy()
        col_options.pop("csv_col_name", None)
        col_options.pop("csv_col_type", None)
        col_options.pop("csv_map_col_nm", None)
        tbl_cols.append({
            "col_id": col.col_id,
            "col_options": col_options
        })
    viewps.tbl_cols.set(tbl_cols)
