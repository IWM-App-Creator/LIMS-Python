from fastapi import HTTPException

def raiseAPIError(message, status_code = 401):
    raise HTTPException (
        status_code = status_code,
        detail={
            "status": False,
            "message": message
        }
    )