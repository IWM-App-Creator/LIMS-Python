from fastapi import APIRouter

from app.endpoints.v1.users import router as user_router
from app.endpoints.v1.pdf import router as pdf_router
from app.endpoints.v1.barcode import router as barcode_router


def getRouter():
    api_router = APIRouter()

    api_router.include_router(user_router, prefix="/users", tags=["Users"])
    api_router.include_router(pdf_router, prefix="/pdf", tags=["PDF"])
    api_router.include_router(barcode_router, prefix="/barcode", tags=["Barcode"])

    return api_router