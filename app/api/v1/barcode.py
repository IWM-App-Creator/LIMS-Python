from io import BytesIO
from fastapi import APIRouter, HTTPException
from barcode import Code128
from barcode.writer import ImageWriter
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from pathlib import Path
from PIL import Image
import os
import time
import cv2

from app.utils.config import BARCODE_OUTPUT_DIR, PDF_OUTPUT_DIR, TEMPLATES_BASE_DIR

router = APIRouter()

templates = Environment(
    loader=FileSystemLoader(
        Path(TEMPLATES_BASE_DIR) / "app" / "templates"
    )
)

def generate_barcode(text: str):
    filename = f"barcode_{int(time.time()*1000)}"
    filepath = os.path.join(BARCODE_OUTPUT_DIR, filename)
    barcode = Code128(text,writer=ImageWriter())
    saved_file = barcode.save(filepath)
    return saved_file

def render_barcode_label(template_name, barcode_path, title):
    template = templates.get_template(template_name)
    return template.render(barcode_img=barcode_path, barcode_title=title)

@router.get("/barcode-pdf")
def barcode_pdf(labelstr: str = "ABC", barcodelbl: str = "ID ABC LBL 2", pdflabel: str = "ZD220", printno: int = 1):

    if pdflabel == "ZD220":
        page_style = """
        @page { size: 189px 94px; margin:0; }
        """
    elif pdflabel == "ZD421_1":
        page_style = """
        @page { size: 152px 106px; margin:0; }
        """
    else: # ZD421_2
        page_style = """
        @page { size: 223px 38px; margin:0; }
        """

    html = f"""
    <html>
    <head>
        <style>
        {page_style}
        body {{ margin:0; padding:0; font-family:Arial; }}
        table {{ border-collapse: collapse; }}
        </style>
    </head>
    <body>
    """

    items = labelstr.split(",")
    labels = barcodelbl.split(",")

    if pdflabel == "ZD220":
        for idx, item in enumerate(items):
            barcode_img = generate_barcode(item)
            title = (labels[idx] if idx < len(labels) else item)

            for _ in range(printno):
                html += render_barcode_label("barcodezd220.html", barcode_img, title)

    elif pdflabel == "ZD421_1":
        for idx, item in enumerate(items):
            barcode_img = generate_barcode(item)
            title = ( labels[idx] if idx < len(labels) else item)

            for _ in range(printno):
                html += render_barcode_label("barcodezd421_1.html", barcode_img, title)
    
    else: # ZD421_2

        html += """
        <table cellpadding="0"
               cellspacing="0">
        """

        count = 0
        for idx, item in enumerate(items):
            barcode_img = generate_barcode(item)
            title = (labels[idx] if idx < len(labels) else item)

            for _ in range(printno):
                if count % 2 == 0:
                    html += "<tr>"

                html += render_barcode_label("barcodezd421_2.html", barcode_img, title)

                if count % 2 == 1:
                    html += "</tr>"

                count += 1
        if count % 2 == 1:
            html += render_barcode_label("barcodezd421_2.html", "", "")
            html += "</tr>"

        html += "</table>"
    
    html += """
    </body>
    </html>
    """

    file_name = f"LIMS_{int(time.time())}.pdf"
    file_path = PDF_OUTPUT_DIR / file_name    

    with open(file_path, "wb") as pdf_file:
        result = pisa.CreatePDF(html, dest=pdf_file)

    if result.err:
        raise HTTPException( status_code=500, detail="PDF generation failed")
    
    return {
        "fetch_flag": "1",
        "message": "Barcode PDF generated",
        "file_name": file_name,
        "pdf_url": f"app/assets/generated_pdfs/{file_name}"
    }

@router.get("/barcode-read")
def read_barcode(file_name: str = "barcode_1782194976544.png"):

    file_path = os.path.join("app","assets","generated_barcodes",file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Barcode image not found")

    try:
        import pyzbar.pyzbar as zbar
        decode = zbar.decode
        # from pyzbar.pyzbar import decode
        image = Image.open(file_path)
        decoded_objects = decode(image)
        if not decoded_objects:
            return {
                "fetch_flag": "0",
                "message": "No Barcode/QR found",
                "file_name": file_name
            }

        barcode = decoded_objects[0]

        return {
            "fetch_flag": "1",
            "message": "Barcode read successfully",
            "file_name": file_name,
            "barcode_type": barcode.type,
            "barcode_value": barcode.data.decode("utf-8")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ZBar load failed: {str(e)}"
            # detail=str(e)
        )
    
@router.get("/barcode-read2")
def read_barcode(file_name: str = "barcode_1782194976544.png"):
    

    file_path = os.path.join("app","assets","generated_barcodes", file_name)
    img = cv2.imread(file_path)
    img = cv2.resize(img, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)

    if img is None:
        return {
            "fetch_flag": "0",
            "message": "Image not found or invalid path",
            "file_name": file_name
        }

    detector = cv2.barcode.BarcodeDetector()
    result = detector.detectAndDecode(img)
    print(result)
    # ok, decoded, points = detector.detectAndDecode(img)

    # if not ok or not decoded:
    #     return {
    #         "fetch_flag": "0",
    #         "message": "No Barcode found",
    #         "file_name": file_name
    #     }

    return {
        "fetch_flag": "1",
        "message": "Barcode read successfully",
        "file_name": file_name,
        # "barcode_value": decoded
    }  


