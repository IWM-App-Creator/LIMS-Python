from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, userps
from app.dbfunctions.dbtablesfunctions import getLastColValFromTbl

def getTestData(request: Request):
    print("getTestData --> ")
    menu_rank = getLastColValFromTbl("sys_dynamic_menu", "rank", (DB.getTableMeta("sys_dynamic_menu").c.created_by == userps.user_id.get()), "rank", "desc")
    print("menu_rank --> ", menu_rank)

def saveTestData (request: Request):
    print("saveTestData --> ")
