from fastapi import APIRouter
from app.controllers.v1 import user_controller as usersapi

router = APIRouter(prefix="/v1")

ROUTES = [
    ("/login", usersapi.login, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)