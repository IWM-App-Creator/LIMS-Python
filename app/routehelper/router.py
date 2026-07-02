from sys import prefix

from fastapi import APIRouter

from app.endpoints.v1.auth import router as auth_router
from app.endpoints.v1.users import router as user_router
from app.endpoints.v1.log import router as log_router

from app.endpoints.v1.rushi import router as rushi_router



def routerGroup():

    apirouter = APIRouter()
    prefix = "/api/v1"
    
    apirouter.include_router(auth_router, prefix = prefix, tags = ["Auth"])
    apirouter.include_router(user_router, prefix = prefix, tags = ["Users"])
    apirouter.include_router(log_router, prefix = prefix, tags = ["Log"])

    apirouter.include_router(rushi_router, prefix = prefix, tags = ["Rushi"])

    # apirouter.include_router(log_router, prefix="/view", tags=["Log"])
    # apirouter.include_router(log_router, prefix="/workspace", tags=["Log"])
    # apirouter.include_router(log_router, prefix="/association", tags=["Log"])

    return apirouter