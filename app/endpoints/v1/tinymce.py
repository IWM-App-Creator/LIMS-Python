from fastapi import APIRouter
from app.controllers.v1 import tinymcecontroller as tinymceapi

router = APIRouter(prefix = "/tinymce")

ROUTES = [
    ("/imgsave", tinymceapi.uploadImage, ["GET"])
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)