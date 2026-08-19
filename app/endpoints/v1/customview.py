from fastapi import APIRouter
from app.controllers.v1 import customviewcontroller as customviewapi

router = APIRouter(prefix = "/customview")

ROUTES = [
    ("/save", customviewapi.saveCustomView, ["POST"])
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)