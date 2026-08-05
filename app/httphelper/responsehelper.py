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

def disable_cache(response):
    response.headers["Cache-Control"] = "private, no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

def cache_for_day(response):
    response.headers["Cache-Control"] = "public, max-age=86400"

# CACHE_ROUTES = {
#     "/api/v1/countries": 86400,
#     "/api/v1/states": 86400,
#     "/api/v1/unit": 86400,
# }

# @app.middleware("http")
# async def cache_control(request: Request, call_next):
#     response = await call_next(request)

#     if request.url.path in CACHE_ROUTES:
#         response.headers["Cache-Control"] = f"public, max-age={CACHE_ROUTES[request.url.path]}"
#     else:
#         response.headers["Cache-Control"] = "private, no-store, no-cache, must-revalidate, max-age=0"
#         response.headers["Pragma"] = "no-cache"
#         response.headers["Expires"] = "0"

#     return response