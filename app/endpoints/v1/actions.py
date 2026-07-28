from fastapi import APIRouter
from app.controllers.v1 import actionscontroller as actionapi

router = APIRouter(prefix = "/actions")

ROUTES = [
    ("/get", actionapi.getActions, ["GET"])
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)