import os
from fastapi import Request
from fastapi.responses import JSONResponse
from app.httphelper.publicendpoints import isPublicEndpoint
from app.helper.authfunctions import authfnct
from app.helper.generalfunctions import getHostName
from app.properties.globalproperties import globalps
from app.properties.usersproperties import userps

async def auth_handler(request: Request, call_next):
    print("auth_handler --> ", request.url.path)
    getHostName(request) # Get Host
    # Skip public APIs
    if isPublicEndpoint(request.url.path):
        return await call_next(request)

    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzc5MiIsInJvbGVfaWQiOiIxIiwiZW1haWwiOiJkaXBha2JlcmFpdEBnbWFpbC5jb20iLCJleHAiOjE3ODU0MjkzNDd9.IjW8IwZTcFIK88iGW8bxM4q5TJQcGKUY4JHpC7yeFHY"
    # payload = authfnct.verifyJWTToken(token)
    # print("payload --> ", payload)
    # Validate Header
    if globalps.IS_LOCAL_DEV == "1": # Bypass auth for local development
        userps.user_id.set(globalps.JWT_USER_ID) # Set a default user_id for local development
        userps.req_subdomain.set("testws1") # Set a default user_id for local development
        userps.role_id.set("1") # Set a default role_id for local development
        # Continue request
        response = await call_next(request)
        # return await call_next(request)
        # Issue refreshed JWT
        new_token = authfnct.createJWTToken(
            user_id=int(globalps.JWT_USER_ID),
            role_id=int("1"),
            email = "chintanit22@gmail.com",
        )
        response.headers["X-New-JWT"] = new_token
        # print("X-New-JWT --> ", response.headers.get("X-New-JWT"))
        return response
    else :
        print("Else request.headers --> ", request.headers)
        auth = request.headers.get("Authorization")
        print("Else auth --> ", auth)
        if not auth:
            return JSONResponse (
                status_code = 403,
                content = {
                    "status": False,
                    "req_host": userps.req_host.get(),
                    "req_subdomain": userps.req_subdomain.get(),
                    "message": "Authorization header missing -- " + request.url.path,
                }
            )
        if not auth.startswith("Bearer "):
            return JSONResponse (
                status_code = 403,
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
        # Set user_id in global properties for global access
        userps.user_id.set(payload["user_id"])
        userps.role_id.set(payload["role_id"])
        request.state.jwt = token

        # Continue request
        response = await call_next(request)

        # Issue refreshed JWT
        new_token = authfnct.createJWTToken(
            user_id=int(payload["user_id"]),
            role_id=int(payload["role_id"]),
            email=payload["email"],
        )

        response.headers["X-New-JWT"] = new_token
        # print("X-New-JWT --> ", response.headers.get("X-New-JWT"))
        return response
        # return await call_next(request)