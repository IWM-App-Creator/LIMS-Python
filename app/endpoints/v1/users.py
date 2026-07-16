from fastapi import APIRouter
from app.controllers.v1 import usercontroller as usersapi

router = APIRouter(prefix = "/user")

ROUTES = [
    ("/getdetail", usersapi.getUserDetail, ["GET"]),
    ("/updateprofile", usersapi.updateUserProfile, ["POST"]),
    ("/getlist", usersapi.getUserList, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods = methods)