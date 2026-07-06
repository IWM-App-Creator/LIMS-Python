from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, globalps
from app.properties.viewproperties import viewps
from app.dbfunctions.viewfunctions import getViewDataByID
from app.function.viewhelper import setViewDataProperties, parseViewOptions

# http://xytovet.localhost:8000/api/v1/view/getdata
def getViewData (request: Request):

    # $dvps->user_id = empty(Input::get('user_id')) ? "1" : Input::get('user_id');
    # $dvps->view_id = empty(Input::get('view_id')) ? "0" : Input::get('view_id');
    # $dvps->callfrom = empty(Input::get('callfrom')) ? "" : Input::get('callfrom'); /* API Call From  */
    # $dvps->tab_id = empty(Input::get('tab_id')) ? "0" : Input::get('tab_id');
    # $dvps->page_no = empty(Input::get('page_no')) ? "1" : Input::get('page_no');
    # $dvps->txtsearch = empty(Input::get('txtsearch')) ? "" : Input::get('txtsearch');
    # $dvps->filterqry = empty(Input::get('filterqry')) ? "" : Input::get('filterqry'); /* Filter Query */
    userview = getViewDataByID(viewps) # Execute Function to User Get Data
    viewps.userview.set(userview)
    
    # $dvps->qry_callfrm = "ViewData";
    setViewDataProperties(viewps) # Set View Properties
    parseViewOptions(viewps)


    # $MigrateScriptFunctions->setViewDataProperties($dvps); /*  */
    # $view_cols = json_decode($dvps->view_cols);
    # $view_cols = $view_cols->view_cols;
    # $col_id_arr = array();
    # foreach($view_cols as $col) {
    #     array_push($col_id_arr, $col->col_id);
    # }
    # $col_id_arr = array_unique($col_id_arr);
    # /* Table Col */
    # $dvps->tbl_cols = array();
    # $tblcol = DB::table('sys_new_db_tables_cols')->whereIn('col_id', $col_id_arr)->where('is_delete', 0)->get();
    # foreach($tblcol as $col) { 
    #     $col_options = $col->col_options;
    #     $tmpopt = json_decode($col_options, true);
    #     unset($tmpopt['csv_col_name'], $tmpopt['csv_col_type'], $tmpopt['csv_map_col_nm']);
    #     $col_options = json_encode($tmpopt);
    #     $tmparr = array();
    #     $tmparr['col_id'] = $col->col_id;
    #     $tmparr['col_options'] = $col_options;
    #     array_push($dvps->tbl_cols, $tmparr);
    # }
    # /* Layout Data */
    # $viewlayout = DB::table('sys_view_layout_users')->where('view_id', $dvps->view_id)->where('is_delete', 0)->first();
    # if($viewlayout) {
    #     $dvps->col_metadata = json_decode($viewlayout->col_metadata);
    #     $dvps->col_colors = json_decode($viewlayout->col_colors);
    #     $dvps->action_group_list = json_decode($viewlayout->action_group_list);
    #     $dvps->user_setting = json_decode($viewlayout->user_setting);
    # }
    
    print("getViewData --> ", viewdata)

# http://xytovet.localhost:8000/api/v1/view/savetbldata
def saveTableData (request: Request):
    print("saveTableData --> ")

# http://xytovet.localhost:8000/api/v1/view/create
def createBlankView (request: Request):
    print("createBlankView --> ")

# http://xytovet.localhost:8000/api/v1/view/getlist
def getViewList (request: Request):
    print("getViewList --> ")

# http://xytovet.localhost:8000/api/v1/view/childstatus
def getViewChildStatus (request: Request):
    print("getViewChildStatus --> ")


# http://xytovet.localhost:8000/api/v1/view/duplicate
def duplicateFullView (request: Request):
    print("duplicateFullView --> ")

# http://xytovet.localhost:8000/api/v1/view/duplicateitem
def duplicateItemData (request: Request):
    print("duplicateItemData --> ")

# http://xytovet.localhost:8000/api/v1/view/lookupdata
def getLookupData (request: Request):
    print("getLookupData --> ")

# http://xytovet.localhost:8000/api/v1/view/filterdata
def getDataForFilter (request: Request):
    print("getDataForFilter --> ")


# http://xytovet.localhost:8000/api/v1/view/getquery
def getRawViewQuery (request: Request):
    print("getRawViewQuery --> ")

# http://xytovet.localhost:8000/api/v1/view/checkurl
def getViewURL (request: Request):
    print("getViewURL --> ")




    