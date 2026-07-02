from urllib import request

from fastapi import Request
from sqlalchemy import select
from app.requesthelper.requesthelper import RequestData
from app.dbhelper.db_helper import DB

from app.properties.globalproperties import globalps
from app.properties.logproperties import logps
from app.functions import logfunctions as logfnct

def getLog():
    # users = DB.tableMeta("users")
    return {
        "fetch_flag": "3",
        # "access_token": access_token,
        # "user_id": usrproperties.user_id,
        # "first_name": usrproperties.first_name,
        # "last_name": usrproperties.last_name,
        # "itm_list": [user],
    }

# def saveLog(token: str):
#     print(f"Token received: {token}")
    # result = verify_token(token)
    # return result

async def saveLog(request: Request):
    print("IS_LOCAL_DEV --> ", globalps.IS_LOCAL_DEV)

    print("saveLog user_id --> ", globalps.user_id)
    print("saveLog workspace_id --> ", globalps.workspace_id)
    print("saveLog workspace_name --> ", globalps.workspace_name)
    print("saveLog ws_url --> ", globalps.ws_url)
    print("saveLog schema_name --> ", globalps.schema_name)
    
    params = RequestData.params(request)
    print("request -->", params)
    # print("request -->", params["view_id"])
    sys_dynamic_view = DB.tableMeta("sys_dynamic_view").alias("sdv")
    stmt = (
        select(sys_dynamic_view)
            .where(sys_dynamic_view.c.is_delete == 0)
    )
    # print("stmt --> ", stmt)
    row = DB.executeDBSelectSingle(stmt)
    print("row --> ", row)
    # view_id = params.get("view_id")
    # user_id = params.get("user_id")
    # print("saveLog view_id -->", view_id)
    # print("saveLog user_id -->", user_id)