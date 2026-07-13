from app.utils.common import DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, nowWithTimeZone, userps
from app.properties.dbproperties import dbps
from app.dbfunctions.viewfunctions import getViewDataByID
from app.dbfunctions.viewlayoutfunctions import getViewLayoutDataByID
from app.helper.viewhelper import viewhlp
from app.helper.viewlayouthelper import setViewLayoutParam
from app.properties.viewproperties import viewps
from app.properties.viewlayoutproperties import viewlyps

# http://xytovet.localhost:8000/api/v1/view/getdata
def setJoinTblColor (request: Request):
    try:
        # params = RequestData.params(request)
        # viewhlp.setViewInputParam(viewps, params) # Get Input Param Data
        # getViewDataByID(viewps) # Get View Data
        # viewdata = getViewDataByID(dbps) # Execute Function to User Get Data
        print("setJoinTblColor --> ")
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)


# miidata/api/dyncol/add?user_id=3779&api_secret=w@lHB)6*2AVsZf.spyff&view_id=181&col_id=0&tab_id=0&all_usr_flg=1&col_type=Status&col_name=status_2&col_alias=Status 2&txt_data_type=int&txtcol_length=4&txtcol_index=1&txtcol_dval=0&is_private=0&dync_cat_id=0&orderflag=Right&ordercol_id=3272&notify_user=0