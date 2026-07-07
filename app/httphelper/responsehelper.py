from fastapi import HTTPException
from app.dbfunctions.logfunctions import saveErrorLog
from app.properties.logproperties import logps

# raiseAPIError( "Workspace not found", 404, view_id=178, section="getWorkspace", desc="Invalid workspace URL")
def raiseAPIError(message, status_code = 401):
    # try:
    #     logps.error_msg.set(message)
    #     saveErrorLog()
    # except Exception:
    #     # Never let logging prevent the API from returning the error
    #     pass
    raise HTTPException (
        status_code = status_code,
        detail={
            "status": False,
            "message": message
        }
    )