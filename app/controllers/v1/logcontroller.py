from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, globalps

from app.properties.logproperties import logps
from app.functions import logfunctions as logfnct
from app.services.firebase.firebase_service import send_push
from app.properties.usersproperties import userps

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
    # print("saveLog --> ")
    # print("IS_LOCAL_DEV --> ", globalps.IS_LOCAL_DEV)
    # print("saveLog user_id --> ", globalps.user_id)
    # print("saveLog workspace_id --> ", globalps.workspace_id)
    # print("saveLog workspace_name --> ", globalps.workspace_name)
    # print("saveLog ws_url --> ", globalps.ws_url)
    # print("saveLog schema_name --> ", userps.schema_name.get())
    
    params = RequestData.params(request)
    # print("request -->", params)
    # print("request -->", params["view_id"])
    # sys_dynamic_view = DB.tableMeta("sys_dynamic_view").alias("sdv")
    # stmt = (
    #     select(sys_dynamic_view)
    #         .where(sys_dynamic_view.c.is_delete == 0)
    # )
    # # print("stmt --> ", stmt)
    # row = DB.executeDBSelectSingle(stmt)
    # print("row --> ", row)
    # view_id = params.get("view_id")
    # user_id = params.get("user_id")
    # print("saveLog view_id -->", view_id)
    # print("saveLog user_id -->", user_id)

def test_push(token: str):
    response = send_push (
        token = token,
        title = "Test Notification",
        body = "Hello from Python"
    )
    return { "firebase_response": response }
