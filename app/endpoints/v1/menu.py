from fastapi import APIRouter
from app.controllers.v1 import menucontroller as menuapi

router = APIRouter(prefix = "/menu")

ROUTES = [
    ("/get", menuapi.getUserMenu, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)