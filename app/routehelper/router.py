from fastapi import APIRouter

from app.endpoints.v1.users import router as user_router
from app.endpoints.v1.log import router as log_router

def routerGroup():

    apirouter = APIRouter()

    apirouter.include_router(user_router, prefix="/users", tags=["Users"])
    apirouter.include_router(log_router, prefix="/log", tags=["Log"])

    # apirouter.include_router(log_router, prefix="/view", tags=["Log"])
    # apirouter.include_router(log_router, prefix="/workspace", tags=["Log"])
    # apirouter.include_router(log_router, prefix="/association", tags=["Log"])

    return apirouter