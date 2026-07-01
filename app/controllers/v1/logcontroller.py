from fastapi import Request
from sqlalchemy import select

from app.database.db_helper import get_table
from app.database.execute_stmt import execute_stmt
from app.database.execute_query import execute_query
from app.helper.requestdata.requesthelper import RequestData
from app.properties.logproperties import logps
from app.functions import logfunctions as logfnct


def getLog():
    logfnct.heresavelogfunction()
    logfnct.heresavelogfunction2()
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


async def saveLog(request: Request,
                view_id: int,
                user_id: int
            ):
    params = RequestData.params(request)
    # print("request -->", request.state.params)
    view_id = params.get("view_id")
    user_id = params.get("user_id")
    
    print("saveLog view_id -->", view_id)
    print("saveLog user_id -->", user_id)


# async def saveLog(request: Request):
#     await RequestHelper.init(request)
#     view_id = request.state.params.get("view_id")
#     token = request.state.jwt


# @app.api_route("/saveLog", methods=["GET", "POST"])
# async def saveLog(request: Request):
#     data = await get_input(request)

#     print(data["view_id"])
#     print(data.get("user_id"))