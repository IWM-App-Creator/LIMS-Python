from fastapi import APIRouter
from app.controllers.v1 import logcontroller as logapi

router = APIRouter(prefix = "/log")

ROUTES = [
    ("/geterrors", logapi.getErrorLog, ["GET"]),
    ("/saveerror", logapi.saveErrorLog, ["GET"]),
    ("/removeerror", logapi.removeErrorLog, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods = methods)
