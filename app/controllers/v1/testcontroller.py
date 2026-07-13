from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, userps
from app.helper.menuhelper import getLastMenuRankByCMID
from app.properties.menuproperties import menups

def getTestData(request: Request):
    print("getTestData --> ")
    menups.m_centre_id.set(61)
    getLastMenuRankByCMID(menups)
    print("rank --> ", menups.last_menu_rank.get())
    

def saveTestData (request: Request):
    print("saveTestData --> ")
