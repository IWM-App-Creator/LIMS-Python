import os
from fastapi import Request
from fastapi.responses import JSONResponse
from app.functions.authfunctions import verifyJWTToken
from app.properties.usersproperties import userps

PUBLIC_APIS = {
    "/auth",
    "/log/v1/save",
    "/docs",
    "/openapi.json",
    "/redoc"
}

async def auth_handler(request: Request, call_next):
    # Skip public APIs
    if request.url.path in PUBLIC_APIS:
        return await call_next(request)

    if os.getenv('IS_LOCAL_DEV') is 1 :
        return await call_next(request)
    else :
        auth = request.headers.get("Authorization")
        if not auth:
            return JSONResponse (
                status_code = 401,
                content = {
                    "status": False,
                    "message": "Authorization header missing"
                }
            )
        if not auth.startswith("Bearer "):
            return JSONResponse (
                status_code = 401,
                content = {
                    "status": False,
                    "message": "Invalid Authorization header"
                }
            )
        token = auth.replace("Bearer ", "", 1)

        # Verify the token using the verify_token function from authfunctions.py
        payload = verifyJWTToken(token)
        if payload is None:
            return JSONResponse (
                status_code = 401,
                content = {
                    "status": False,
                    "message": "Invalid or expired token"
                }
            )
        request.state.user_id = payload["user_id"]
        userps.user_id = payload["user_id"]  # Set user_id in user properties for global access
        # request.state.email = payload["email"]   # Optional
        request.state.jwt = token
        return await call_next(request)