from fastapi import Request
from fastapi.responses import JSONResponse

async def error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response

    except Exception as ex:
        # TODO: Save to database or log file
        print(ex)

        return JSONResponse(
            status_code=500,
            content={
                "status": False,
                "message": "Internal Server Error",
                "error": str(ex)
            }
        )