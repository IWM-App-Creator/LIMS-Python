from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, globalps
import json
from app.properties.viewproperties import viewps
from app.properties.dbproperties import dbps
from app.dbfunctions.dbtablesfunctions import getDBTableData
from app.dbfunctions.viewfunctions import getViewDataByID
from app.dbfunctions.viewlayoutfunctions import getViewLayoutDataByID
from app.functions.viewhelper import setViewInputParam, setViewDataProperties, setViewTableCols, setViewLayout

# http://xytovet.localhost:8000/api/v1/view/getdata?view_id=178
def getViewData (request: Request):
    try:
        params = RequestData.params(request)
        setViewInputParam(viewps, params) # Get Input Param Data
        getViewDataByID(viewps) # Get View Data
        if not viewps.userview.get(): # Invalid View
            raiseAPIError("View Not Found", 401)
        setViewDataProperties(viewps) # Set View Properties
        setViewTableCols(viewps) # Get View Columns
        setViewLayout(viewps) # Get View Layout Data
        # --------------------------
        # Process To Get View Data
        # --------------------------

        # /* Get Data */
        # $GeneralFunctions->sortObjectsByKey($view_cols, 'rank', 'asc'); /* Sort By Rank */
        # $dvps->view_cols = $view_cols;
        # $dataarr = array();
        # $dvps->dataarr = $dataarr;
        # try {
        #     $dvps->rawqry = "";
        #     if($dvps->txtsearch) {
        #         $this->getViewSearchQuery($dvps);
        #         // $DynamicViewFunctions->appendChildViewSearchQuery($dvps); /* Search For Child View */
        #         if($dvps->rawqry) {
        #             $dvps->view_qry = $dvps->view_qry . " and ( " . $dvps->rawqry . " ) ";
        #         }
        #     }
        #     if($dvps->filterqry) {
        #         $this->getViewFilteredQuery($dvps);
        #     }
        #     // if($dvps->association_limit) {
        #     //     $DynamicViewFunctions->getViewAssociationLimit($dvps);
        #     // }
        #     // checkViewAssociation. 
        #     $dvps->sorting = "mtbl." . $dvps->primary_colnm . " DESC";
        #     $dvps->offset = 0;
        #     $this->setViewPagingSorting($dvps);
        #     if($dvps->sorting) {
        #         $dvps->view_qry = $dvps->view_qry . " order by " . $dvps->sorting;
        #     }
        #     $dvps->view_qry = $dvps->view_qry . " limit " . $dvps->offset . ', ' . $dvps->page_size;
        #     // echo "<br/><br/> view_qry --> " . $dvps->view_qry;
        #     // exit;
        #     $dvps->dataarr = DB::select($dvps->view_qry); /* Execute Query To Get View Data */
        #     $this->getRecordCount($dvps); /* Get Total Record Count */
        #     $this->setViewItemArray($dvps); /* Set View Data In Items Array */
        # } catch (\Exception $e) {
        #     echo "<br/><br/> Exception --> " . $e->getMessage();
        #     $dataarr = array();
        #     exit;
        # }
        # $this->setViewOutputArray($dvps); /* Output Json */
    except Exception as e:
        raiseAPIError(str(e), 500)

    # print("getViewData --> ", viewdata)

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




    