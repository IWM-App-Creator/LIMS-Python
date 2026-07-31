from fastapi import APIRouter
from app.controllers.v1 import filtercontroller as filtersapi

router = APIRouter(prefix = "/filter")

ROUTES = [
    ("/get", filtersapi.getFilters, ["GET"])
    ("/save", filtersapi.saveViewFilter, ["POST"])
    ("/copy", filtersapi.copySaveFilterView, ["POST"])
    ("/setdefault", filtersapi.makeDefaultFilter, ["POST"])
    ("/remove", filtersapi.removeSaveFilterView, ["POST"])
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)