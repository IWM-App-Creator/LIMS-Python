from fastapi import APIRouter
from app.controllers.v1 import widgetcontroller as widgetapi

router = APIRouter(prefix = "/widget")

ROUTES = [
    ("/get", widgetapi.getWidgetList, ["GET"]),
    ("/getuser", widgetapi.getUserWidgetList, ["GET"]),
    ("/category", widgetapi.getWidgetCategory, ["GET"]),
    ("/share", widgetapi.shareUserWidget, ["POST"]),
    ("/saveuser", widgetapi.saveUserWidget, ["GET"]),
    ("/saveview", widgetapi.saveViewWidget, ["POST"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)