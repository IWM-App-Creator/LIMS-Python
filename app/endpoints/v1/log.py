from fastapi import APIRouter
from app.controllers.v1 import logcontroller as logapi

router = APIRouter(prefix="/log")

ROUTES = [
    ("/get", logapi.getLog, ["GET"]),  #@app.api_route("/saveLog", methods=["GET", "POST"])
    ("/save", logapi.saveLog, ["GET"]),
    # ("/remove", logapi.removeLog, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)