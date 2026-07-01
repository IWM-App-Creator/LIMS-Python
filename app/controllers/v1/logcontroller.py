from fastapi import Request
from sqlalchemy import select

# from app.database.db_helper import get_table
# from app.database.execute_stmt import execute_stmt
# from app.database.execute_query import execute_query
from app.requesthelper.requesthelper import RequestData

from app.properties.logproperties import logps
from app.functions import logfunctions as logfnct


def getLog():
    
    # users = DB.table(request, "users")
    # orders = DB.table(request, "orders")
    # products = DB.table(request, "products")
    # users = DB.get_table("users", request.state.schema)

    # print(request.state.schema)
    # print(request.state.workspace_id)

    # logfnct.heresavelogfunction()
    # logfnct.heresavelogfunction2()
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
    params = RequestData.params(request)
    # print("request -->", request.state.params)

    # user_id = request.state.user_id # From the auth middleware, if you want to get the user_id from the token

    view_id = params.get("view_id")
    user_id = params.get("user_id")
    print("saveLog view_id -->", view_id)
    print("saveLog user_id -->", user_id)