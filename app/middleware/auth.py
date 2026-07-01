from app.functions.authfunctions import verify_token
from fastapi import Request
from fastapi.responses import JSONResponse

PUBLIC_APIS = {
    "/login",
    "/docs",
    "/openapi.json",
    "/redoc"
}

async def auth_middleware(request: Request, call_next):
    # Skip public APIs
    if request.url.path in PUBLIC_APIS:
        return await call_next(request)
    auth = request.headers.get("authorization")
    if not auth:
        return JSONResponse(
            status_code=401,
            content={
                "status": False,
                "message": "Authorization header missing"
            }
        )
    if not auth.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={
                "status": False,
                "message": "Invalid Authorization header"
            }
        )
    token = auth.replace("Bearer ", "", 1)
    user = verify_token(token)
    if user is None:
        return JSONResponse(
            status_code=401,
            content={
                "status": False,
                "message": "Invalid or expired token"
            }
        )
    # Save authenticated user for controllers/services
    request.state.user = user
    request.state.jwt = token
    return await call_next(request)