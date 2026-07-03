from fastapi import APIRouter
from app.controllers.v1 import workspacecontroller as wsapi

router = APIRouter(prefix = "/workspace")

ROUTES = [
    ("/getlist", wsapi.getTestData, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)