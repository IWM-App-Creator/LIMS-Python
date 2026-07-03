from fastapi import APIRouter
from app.controllers.v1 import authcontroller as authapi

router = APIRouter(prefix = "/auth")

# http://127.0.0.1:8000/api/v1/auth/login?email=chintanit22%40gmail.com&password=1234567890
# http://127.0.0.1:8000/api/v1/auth/validatejwt?token=
# http://127.0.0.1:8000/api/v1/auth/forgotpassword?email=chintanit22%40gmail.com
# http://127.0.0.1:8000/api/v1/auth/resetpassword?token=&new_password=1234567890&confirm_password=1234567890

ROUTES = [
    ("/login", authapi.doLogin, ["GET"]),
    ("/validatejwt", authapi.validateJWT, ["GET"]),
    ("/forgotpassword", authapi.forgotPassword, ["POST"]),
    ("/resetpassword", authapi.resetPassword, ["POST"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)