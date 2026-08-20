import os
from fastapi import Request
from fastapi.responses import JSONResponse
from app.httphelper.publicendpoints import isPublicEndpoint
from app.helper.authfunctions import authfnct
from app.helper.generalfunctions import getHostName
from app.properties.globalproperties import globalps
from app.properties.usersproperties import userps

async def auth_handler(request: Request, call_next):
    getHostName(request) # Get Host
    # Skip public APIs
    if isPublicEndpoint(request.url.path):
        return await call_next(request)

    # Validate Header
    if globalps.IS_LOCAL_DEV == "1": # Bypass auth for local development
        userps.user_id.set(globalps.JWT_USER_ID) # Set a default user_id for local development
        userps.req_subdomain.set("xytovet") # Set a default user_id for local development
        userps.role_id.set("1") # Set a default role_id for local development

        # auth = request.headers.get("Authorization")
        # if auth: 
        #     token = auth.replace("Bearer ", "", 1)
        #     payload = authfnct.verifyJWTToken(token)
        #     jwt_payload = payload["payload"]
        #     userps.user_id.set(jwt_payload["user_id"])
        #     userps.role_id.set(jwt_payload["role_id"])

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
        return response
    else :
        auth = request.headers.get("Authorization")
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
        print("token --> ", token)
        # Verify the token using the verify_token function from authfunctions.py
        payload = authfnct.verifyJWTToken(token)
        # if payload is None:
        if not payload["status"]:
            return JSONResponse (
                status_code = 401,
                content = {
                    "status": False,
                    "message": "Invalid or expired token"
                }
            )
        # Set user_id in global properties for global access
        jwt_payload = payload["payload"]
        userps.user_id.set(jwt_payload["user_id"])
        userps.role_id.set(jwt_payload["role_id"])
        print("user_id --> ", userps.user_id.get())
        print("role_id --> ", userps.role_id.get())
        request.state.jwt = token
        # Continue request
        response = await call_next(request)

        # Issue refreshed JWT
        # new_token = authfnct.createJWTToken(
        #     user_id=int(jwt_payload["user_id"]),
        #     role_id=int(jwt_payload["role_id"]),
        #     email=jwt_payload["email"],
        # )
        # response.headers["X-New-JWT"] = new_token
        # print("X-New-JWT --> ", response.headers.get("X-New-JWT"))

        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        return response
        # return await call_next(request)