from fastapi import APIRouter
from app.controllers.v1 import systemviewcontroller as systemviewapi

router = APIRouter(prefix = "/systemview")

ROUTES = [
    ('/get', systemviewapi.getSystemViewList, ['GET']),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods = methods)