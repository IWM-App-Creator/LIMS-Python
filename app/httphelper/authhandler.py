import os
from fastapi import Request
from fastapi.responses import JSONResponse
from app.httphelper.publicendpoints import isPublicEndpoint
from app.functions.authfunctions import authfnct
from app.functions.generalfunctions import getHostName
from app.properties.globalproperties import globalps
from app.properties.usersproperties import userps

async def auth_handler(request: Request, call_next):
    print("auth_handler --> ")
    getHostName(request) # Get Host
    # Skip public APIs
    if isPublicEndpoint(request.url.path):
        return await call_next(request)

    # Validate Header
    if globalps.IS_LOCAL_DEV == "1": # Bypass auth for local development
        userps.user_id.set(globalps.JWT_USER_ID) # Set a default user_id for local development
        userps.role_id.set("1") # Set a default role_id for local development
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
        userps.user_id.set(payload["user_id"])  # Set user_id in global properties for global access
        userps.role_id.set(payload["role_id"])
        request.state.jwt = token
        return await call_next(request)