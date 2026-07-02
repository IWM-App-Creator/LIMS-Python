from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, globalps

def getDataRushiTest (request: Request, param1: str, param2: str):
    print("getDataRushiTest --> ")
    # print("getDataRushiTest --> ", param1)
    # params = RequestData.params(request)
    # print("request -->", params["view_id"])

    # tbluser = DB.getTableMeta("users", "systemconfig").alias("usr")
    # stmt = (
    #     select(tbluser)
    #         .where(tbluser.c.email == email)
    # )
    # user = DB.executeDBSelectSingle(stmt)

    # sys_dynamic_view = DB.getTableMeta("sys_dynamic_view", "9m8i7azboj").alias("sdv")
    # stmt = (
    #     select(sys_dynamic_view)
    #         .where(tbluser.c.email == email)
    # )
    # user = DB.executeDBSelectSingle(stmt)
    # sys_dynamic_view = DB.tableMeta("sys_dynamic_view").alias("sdv") # Current based on subdomain..
    

def saveDataRushiTest (request: Request):
    print("getDataRushiTest --> ")
    # print("getDataRushiTest --> ", param1)
    # params = RequestData.params(request)
    # print("request -->", params["view_id"])