from fastapi import APIRouter
from app.controllers.v1 import authcontroller as authapi

router = APIRouter(prefix = "/auth")

ROUTES = [
    ("/login", authapi.doLogin, ["GET"]),
    ("/validatejwt", authapi.validateJWT, ["GET"]),
    ("/forgotpassword", authapi.forgotPassword, ["POST"]),
    ("/resetpassword", authapi.resetPassword, ["POST"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)
