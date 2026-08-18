from fastapi import APIRouter
from app.controllers.v1 import viewcsvcontroller as viewcsvapi

router = APIRouter(prefix = "/viewcsv")

ROUTES = [
    ("download", viewcsvapi.downloadCSVData, ["GET"]),
    ("upload", viewcsvapi.uploadCSVData, ["GET"])
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods = methods)
