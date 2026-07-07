import json
from app.utils.common import select, DB, userps

def processInputParam(viewps, params):
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
    print("view_options", viewps.view_options)
    # parseViewOptions(viewps)

def parseViewOptions(viewps):
    viewopt = json.loads(viewps.view_options.get()) if viewps.view_options.get() else {}
    viewps.table_id.set(viewopt.get("table_id", 0))
    viewps.table_name.set(viewopt.get("table_name", 0))
    viewps.view_qry.set(viewopt.get("view_qry", 0))
    viewps.primary_col.set(viewopt.get("primary_col", 0))
    viewps.primary_col.set(viewopt.get("primary_col", 0))
    viewps.delete_col.set(viewopt.get("delete_col", 0))
    viewps.show_deleted.set(viewopt.get("show_deleted", 0))
    viewps.enable_newline.set(viewopt.get("enable_newline", 0))
    viewps.enable_join_save.set(viewopt.get("enable_join_save", 0))
    viewps.is_child_view.set(viewopt.get("is_child_view", 0))
    viewps.enable_child_srch.set(viewopt.get("enable_child_srch", 0))
    viewps.enable_chart.set(viewopt.get("enable_chart", 0))