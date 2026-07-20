from fastapi import HTTPException
from fastapi.responses import JSONResponse

def raiseAPIError(message, status_code = 401):
    raise HTTPException (
        status_code = status_code,
        detail={
            "status": False,
            "message": message
        }
    )

def raiseInvalidError(message, status_code = 401):
    return JSONResponse (
        status_code = status_code,
        content = {
            "status": False,
            "message": message,
        }
    )