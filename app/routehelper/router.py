from sys import prefix

from fastapi import APIRouter

from app.endpoints.v1.auth import router as auth_router

from app.endpoints.v1.workspace import router as workspace_router
from app.endpoints.v1.association import router as association_router
from app.endpoints.v1.dbtable import router as dbtable_router
from app.endpoints.v1.view import router as view_router
from app.endpoints.v1.widget import router as widget_router

from app.endpoints.v1.users import router as user_router
from app.endpoints.v1.log import router as log_router

from app.endpoints.v1.testapi import router as test_router


def routerGroup():

    apirouter = APIRouter()
    prefix = "/api/v1"
    
    apirouter.include_router(auth_router, prefix = prefix, tags = ["Auth"])
    
    apirouter.include_router(workspace_router, prefix = prefix, tags = ["Workspace"])
    apirouter.include_router(association_router, prefix = prefix, tags = ["Association"])
    apirouter.include_router(dbtable_router, prefix = prefix, tags = ["Table"])
    apirouter.include_router(view_router, prefix = prefix, tags = ["View"])
    apirouter.include_router(widget_router, prefix = prefix, tags = ["Widget"])

    apirouter.include_router(user_router, prefix = prefix, tags = ["Users"])
    apirouter.include_router(log_router, prefix = prefix, tags = ["Log"])

    apirouter.include_router(test_router, prefix = prefix, tags = ["Test"])

    return apirouter