from fastapi import APIRouter
from app.controllers.v1 import filtercontroller as filtersapi

router = APIRouter(prefix = "/filter")

ROUTES = [
    ("/get", filtersapi.getFilters, ["GET"])
    ("/save", filtersapi.saveViewFilter, ["POST"])
    ("/setdefault", filtersapi.saveViewFilter, ["POST"])
    ("/remove", filtersapi.saveViewFilter, ["POST"])
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)