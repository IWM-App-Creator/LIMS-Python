from fastapi import APIRouter
from app.controllers.v1 import notescontroller as notesapi

router = APIRouter(prefix = "/notes")

ROUTES = [
    ("/get", notesapi.getUserNotes, ["GET"]),
    ("/save", notesapi.saveUserNote, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)