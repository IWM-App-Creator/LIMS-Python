from fastapi import APIRouter
from app.controllers.v1 import widgetcontroller as widgetapi

router = APIRouter(prefix = "/widget")

ROUTES = [
    ("/getlist", widgetapi.getTestData, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)