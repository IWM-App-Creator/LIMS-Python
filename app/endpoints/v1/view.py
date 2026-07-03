from fastapi import APIRouter
from app.controllers.v1 import viewcontroller as viewapi

router = APIRouter(prefix = "/view")

ROUTES = [
    ("/getlist", viewapi.getTestData, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)