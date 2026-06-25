from fastapi import APIRouter
from app.controllers.v1 import barcode_controller as barcodeapi

router = APIRouter(prefix="/v1")

ROUTES = [
    ("/barcode-pdf", barcodeapi.barcode_pdf, ["GET"]),
    ("/barcode-read", barcodeapi.read_barcode, ["GET"]),
    ("/barcode-read2", barcodeapi.read_barcode2, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)
    
