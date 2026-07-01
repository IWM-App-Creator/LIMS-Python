from fastapi import  HTTPException
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

def saveLog(token: str):
    print(f"Token received: {token}")
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
