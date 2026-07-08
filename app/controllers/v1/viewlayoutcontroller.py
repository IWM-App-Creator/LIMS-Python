from app.utils.common import Request
from app.properties.dbproperties import dbps
from app.dbfunctions.viewfunctions import getViewDataByID

# http://xytovet.localhost:8000/api/v1/view/getdata
def getViewData (request: Request):
    viewdata = getViewDataByID(dbps) # Execute Function to User Get Data
    print("getViewData --> ", viewdata)