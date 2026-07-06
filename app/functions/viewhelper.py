from sqlalchemy import func
from app.utils.common import select, DB, userps
from app.dbfunctions.dbtablesfunctions import getDBTableData

def setViewDataProperties(viewps):
    userview = viewps.userview.get()
    viewps.view_id.set(userview.view_id)
    viewps.view_name.set(userview.view_name)
    viewps.view_url.set(userview.view_url)
    viewps.view_type.set(userview.view_type)
    viewps.view_options.set(userview.view_options)
    viewps.view_cols.set(userview.view_cols)
    viewps.view_joins.set(userview.view_joins)
    viewps.view_child.set(userview.view_child)
    viewps.view_actions.set(userview.view_actions)
    
    # $this->parseViewOptions($dvps);    

def parseViewOptions(viewps):
    print("parseViewOptions")
    # public function parseViewOptions($dvps) {
    #     $viewopt = json_decode($dvps->view_options);
    #     $dvps->table_id = $viewopt->table_id ?? 0;
    #     $dvps->table_name = $viewopt->table_name ?? "";
    #     $dvps->view_qry = $viewopt->view_qry ?? "";
    #     $dvps->primary_col = $viewopt->primary_col ?? "";
    #     $dvps->primary_colnm = explode("|", $viewopt->primary_col)[1];
    #     $dvps->delete_col = $viewopt->delete_col ?? "";
    #     $dvps->show_deleted = $viewopt->show_deleted ?? 0;
    #     $dvps->enable_newline = $viewopt->enable_newline ?? 0;
    #     $dvps->enable_join_save = $viewopt->enable_join_save ?? 0;
    #     $dvps->is_child_view = $viewopt->is_child_view ?? 0;
    #     $dvps->enable_child_srch = $viewopt->enable_child_srch ?? 0;
    #     $dvps->enable_chart = $viewopt->enable_chart ?? 0;
    # }
