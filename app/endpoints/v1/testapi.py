from fastapi import APIRouter
from app.controllers.v1 import testcontroller as testapi

router = APIRouter(prefix = "/testapi")

ROUTES = [
    ("/getlist", testapi.getTestData, ["GET"]),
    ("/save", testapi.saveTestData, ["GET", "POST"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)