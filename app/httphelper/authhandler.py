import os
from fastapi import Request
from fastapi.responses import JSONResponse
from app.functions.authfunctions import authfnct
from app.properties.globalproperties import globalps

PUBLIC_APIS = {
    "/api/v1/auth/login",
    "/docs",
    "/openapi.json",
    "/redoc"
}

async def auth_handler(request: Request, call_next):
    # Skip public APIs
    if request.url.path in PUBLIC_APIS:
        return await call_next(request)

    if globalps.IS_LOCAL_DEV == "1": # Bypass auth for local development
        # globalps.user_id = globalps.JWT_USER_ID  # Set a default user_id for local development
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
        payload = authfnct.verifyJWTToken(token)
        if payload is None:
            return JSONResponse (
                status_code = 401,
                content = {
                    "status": False,
                    "message": "Invalid or expired token"
                }
            )
        # request.state.user_id = payload["user_id"]
        globalps.user_id = payload["user_id"]  # Set user_id in global properties for global access
        request.state.jwt = token
        return await call_next(request)