from sqlalchemy import select
from app.utils.common import DB, JSONResponse, raiseAPIError, globalps

def getUserDetail(token: str):
    print("getUserDetail:", token)

def getUserList():
    print("getUserList:")
