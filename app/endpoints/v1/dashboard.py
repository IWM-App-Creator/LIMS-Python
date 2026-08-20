from fastapi import APIRouter
from app.controllers.v1 import dashboardcontroller as dashboardapi

router = APIRouter(prefix = "/dashboard")

ROUTES = [
    ("/save", dashboardapi.saveUserDashboard, ["POST"])
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)