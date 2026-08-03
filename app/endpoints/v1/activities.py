from fastapi import APIRouter
from app.controllers.v1 import activitiescontroller as activitiesapi

router = APIRouter(prefix = "/activities")

ROUTES = [
    ("/get", activitiesapi.getActivities, ["GET"]),
    ("/revert", activitiesapi.revertActivities, ["GET", "POST"])
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)