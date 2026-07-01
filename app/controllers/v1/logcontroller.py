# from fastapi import HTTPException
# from fastapi import Request
# from fastapi import Header

from urllib import request

from fastapi import APIRouter, Request

from sqlalchemy import select

from app.database.db_helper import get_table
from app.database.execute_stmt import execute_stmt
from app.database.execute_query import execute_query

# from app.functions.authfunctions import create_token, verify_token

from app.properties.logproperties import logps
from app.functions import logfunctions as logfnct

# heresavelogfunction

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

def removeLog(token: str):
    print(f"Token received: {token}")
    # response = send_push(
    #     token=token,
    #     title="Test Notification",
    #     body="Hello from Python"
    # )
    # return { "firebase_response": response }



async def saveLog(request: Request):
    print("saveLog --> ")

    print("request -->", request.state.params)
    # params = request.state.params
    # jwt = request.state.jwt

    # if request.method == "GET":
    #     params = dict(request.query_params)
    # else:
    #     params = await request.json()      # if JSON body
    #     # or:
    #     # params = dict(await request.form())  # if form-data
    # print(params)
    # view_id = params.get("view_id")
    # user_id = params.get("user_id")

    # headers = dict(request.headers)
    # print(headers)
    # print(headers.get("authorization"))


# async def saveLog(request: Request):
#     await RequestHelper.init(request)
#     view_id = request.state.params.get("view_id")
#     token = request.state.jwt


# @app.api_route("/saveLog", methods=["GET", "POST"])
# async def saveLog(request: Request):
#     data = await get_input(request)

#     print(data["view_id"])
#     print(data.get("user_id"))