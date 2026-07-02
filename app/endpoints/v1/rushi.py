from fastapi import APIRouter
from app.controllers.v1 import rushicontroller as rushiapi

router = APIRouter(prefix = "/rushi")

ROUTES = [
    ("/getlist", rushiapi.getDataRushiTest, ["GET"]),
    # ("/save", rushiapi.saveDataRushiTest, ["GET", "POST"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)