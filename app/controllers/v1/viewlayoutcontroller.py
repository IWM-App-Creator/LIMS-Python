from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, globalps
from app.properties.dbproperties import dbps
from app.dbfunctions.viewfunctions import getViewDataByID

# http://xytovet.localhost:8000/api/v1/view/getdata
def getViewData (request: Request):
    viewdata = getViewDataByID(dbps) # Execute Function to User Get Data
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




    