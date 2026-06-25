from fastapi import APIRouter
from app.controllers.v1 import pdf_controller as pdfapi

router = APIRouter(prefix="/v1")

ROUTES = [
    ("/generate-pdf", pdfapi.generate_pdf, ["GET"]),
    ("/generate-watermarked-pdf", pdfapi.generate_watermarked_pdf, ["GET"]),
    ("/print-labels-pdf", pdfapi.print_labels_pdf, ["GET"]),
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)