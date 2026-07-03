from fastapi import APIRouter
from app.controllers.v1 import tablecontroller as tableapi

router = APIRouter(prefix = "/table")

ROUTES = [
    ("/getlist", tableapi.getTestData, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)