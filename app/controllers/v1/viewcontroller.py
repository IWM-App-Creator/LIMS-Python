from app.utils.common import DB, Request, RequestData, JSONResponse, raiseAPIError
from app.properties.viewproperties import viewps
from app.dbfunctions.viewfunctions import getViewDataByID
from app.functions.viewhelper import viewhlp
from app.functions.generalfunctions import sortObjectsByKey

# http://xytovet.localhost:8000/api/v1/view/getdata?view_id=178
def getViewData (request: Request):
    try:
        params = RequestData.params(request)
        viewhlp.setViewInputParam(viewps, params) # Get Input Param Data
        getViewDataByID(viewps) # Get View Data
        if not viewps.userview.get(): # Invalid View
            raiseAPIError("View Not Found", 401)
        viewhlp.setViewDataProperties(viewps) # Set View Properties
        viewhlp.setViewTableCols(viewps) # Get View Columns
        viewhlp.setViewLayout(viewps) # Get View Layout Data
        # --------------------------
        # Sort View Col
        # --------------------------
        view_cols = viewps.view_cols.get()
        sortObjectsByKey(view_cols["view_cols"], 'rank', 'asc'); # Sort By Rank
        viewps.view_cols.set(view_cols)
        # --------------------------
        # Get Data
        # --------------------------
        dataarr = []
        viewps.view_qry_data.set(dataarr)
        view_qry = viewps.view_qry.get() # Get Query
        # print("primary_colnm --", viewps.primary_colnm.get())
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
        sorting = f"mtbl.{viewps.primary_colnm.get()} DESC"
        # viewps.sorting.set(sorting)
        # viewps.primary_colnm.set(0)
        # setViewSorting(viewps) # Get Sorting
        # print("primary_colnm --", viewps.primary_colnm.get())
        #     if($dvps->sorting) {
                # $dvps->view_qry = $dvps->view_qry . " order by " . $dvps->sorting;
        #     }
        view_qry = f"{view_qry} Order By {sorting}"
        viewhlp.setViewPaging(viewps) # Get Paging
        view_qry = f"{view_qry} LIMIT {viewps.offset.get()}, {viewps.page_size.get()}"
        viewps.view_qry.set(view_qry)
        view_qry_data = DB.executeDBStatement(view_qry) # Execute Query To Get View Data
        viewps.view_qry_data.set(view_qry_data)
        viewhlp.getRecordCount(viewps) # Total Record Data
        viewhlp.setViewItemArray(viewps); # Set View Data In Items Array
        viewhlp.setViewOutputArray(viewps); # Output Json
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "View Data",
                "view_data": viewps.output_array.get()
            }
        )
    except Exception as e:
        raiseAPIError(str(e), 500)

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
