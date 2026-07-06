import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

async def error_handler(request: Request, call_next):
    print("error_handler --> ")
    try:
        response = await call_next(request)
        return response
    except Exception as ex:
        logger.exception("Unhandled request error: %s %s", request.method, request.url)
        return JSONResponse (
            status_code = 500,
            content = {
                "status": False,
                "message": "Internal Server Error",
                "error": str(ex)
            }
        )
