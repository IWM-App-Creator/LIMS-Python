from sqlalchemy import select
from app.utils.common import DB, JSONResponse, raiseAPIError, globalps

def getUserList():
    print("getUserList:")
