from fastapi import APIRouter
from app.controllers.v1 import formscontroller as formapi

router = APIRouter(prefix = "/form")

ROUTES = [
    ('/getfield', formapi.getDynamicFormField, ['GET']),
    ('/savefields', formapi.saveFormFields, ['GET']),
    ('/savedata', formapi.saveFormData, ['GET']),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods = methods)