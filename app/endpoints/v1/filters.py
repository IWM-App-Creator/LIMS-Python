from fastapi import APIRouter
from app.controllers.v1 import filtercontroller as filtersapi

router = APIRouter(prefix = "/filters")

ROUTES = [
    ("/get", filtersapi.getFilters, ["GET"])
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)