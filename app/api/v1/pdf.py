from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from pypdf import PdfReader, PdfWriter
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from io import BytesIO
from pathlib import Path
import os
import time

from app.utils.config import PDF_OUTPUT_DIR, TEMPLATES_BASE_DIR

router = APIRouter()

templates = Environment(
    loader=FileSystemLoader(
        Path(TEMPLATES_BASE_DIR) / "app" / "templates"
    )
)

@router.get("/generate-pdf")
def generate_pdf(orientation: str = "portrait"):

    if orientation.lower() == "landscape":
        page_size = landscape(A4)
    else:
        page_size = portrait(A4)

    file_name = f"{orientation}.pdf"
    file_path = PDF_OUTPUT_DIR / file_name

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=page_size
    )

    width, height = page_size

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(
        50,
        height - 50,
        f"{orientation.title()} PDF"
    )

    pdf.save()

    return {
        "fetch_flag": "1",
        "file_name": file_name,
        "file_path": str(file_path),
        "width": width,
        "height": height
    }

@router.get("/generate-watermarked-pdf")
def generate_watermarked_pdf(orientation: str = "portrait"):

    if orientation.lower() == "landscape":
        page_size = landscape(A4)
    else:
        page_size = portrait(A4)

    file_name = f"{orientation}_watermarked.pdf"
    file_path = PDF_OUTPUT_DIR / file_name

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=page_size
    )

    width, height = page_size

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(
        50,
        height - 50,
        f"{orientation.title()} Watermarked PDF"
    )

    # watermark example
    pdf.saveState()
    pdf.setFont("Helvetica-Bold", 60)
    pdf.setFillGray(0.85)
    pdf.translate(width / 2, height / 2)
    pdf.rotate(45)
    pdf.drawCentredString(0, 0, "WATERMARK")
    pdf.restoreState()

    pdf.save()

    return {
        "fetch_flag": "1",
        "file_name": file_name,
        "file_path": str(file_path)
    }

@router.get("/print-labels-pdf")
def print_labels_pdf(labelstr: str = "ITEM1~~LOT1~~12345||ITEM2~~LOT2~~67890", pdflabel: str = "ZD220", printno: int = 1):

    page_style = ""
    if pdflabel == "ZD220":
        page_style = """
        @page { size: 189px 94px; margin: 0; }
        """

    elif pdflabel == "ZD421_1":
        page_style = """
        @page { size: 152px 106px; margin: 0; }
        """

    else:  # ZD421_2
        page_style = """
        @page { size: 223px 38px; margin: 0; }
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            {page_style}
            html, body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                font-family: Arial, sans-serif;
            }}
        </style>
    </head>
    <body>
    """

    items = labelstr.split("||")
    if pdflabel == "ZD220":
        for itm in items:
            if not itm:
                continue

            sub = itm.split("~~")
            for _ in range(printno):
                html += render_label("zd220.html", sub[0] if len(sub) > 0 else "", sub[1] if len(sub) > 1 else "", sub[2] if len(sub) > 2 else "")

    elif pdflabel == "ZD421_1":
        for itm in items:
            if not itm:
                continue

            sub = itm.split("~~")
            for _ in range(printno):
                html += render_label("zd421_1.html", sub[0] if len(sub) > 0 else "", sub[1] if len(sub) > 1 else "", sub[2] if len(sub) > 2 else "")

    else:  # ZD421_2
        html += """
        <table cellspacing="0" cellpadding="0" border="0" style="border-collapse:collapse;">
        """

        count = 0
        for itm in items:
            if not itm:
                continue

            sub = itm.split("~~")
            for _ in range(printno):

                if count % 2 == 0:
                    html += "<tr>"
                html += render_label("zd421_2.html", sub[0] if len(sub) > 0 else "", sub[1] if len(sub) > 1 else "", sub[2] if len(sub) > 2 else "")

                if count % 2 == 1:
                    html += "</tr>"

                count += 1
        if count % 2 == 1:
            html += render_label("zd421_2.html", "", "", "")
            html += "</tr>"

        html += "</table>"

    html += """
    </body>
    </html>
    """

    # Generate filename
    file_name = f"LIMS_{int(time.time())}.pdf"
    file_path = PDF_OUTPUT_DIR / file_name    
    
    with open(file_path, "wb") as pdf_file:
        result = pisa.CreatePDF(html, dest=pdf_file)

    if result.err:
        raise HTTPException( status_code=500, detail="PDF generation failed")

    return {
        "fetch_flag": "1",
        "message": "PDF generated successfully",
        "file_name": file_name,
        "pdf_url": f"{str(file_path)}/{file_name}",

    }

def render_label(template_name: str, item1: str = "", item2: str = "", item3: str = ""):
    template = templates.get_template(template_name)
    return template.render(
        sub_item_1=item1,
        sub_item_2=item2,
        sub_item_3=item3
    )