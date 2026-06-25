from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from pypdf import PdfReader, PdfWriter
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from io import BytesIO
import os
import time

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

templates = Environment(
    loader=FileSystemLoader(
        os.path.join(BASE_DIR, "templates")
    )
)

@router.get("/generate-pdf")
def generate_pdf(orientation: str = "portrait"):

    if orientation.lower() == "landscape":
        page_size = landscape(A4)
    else:
        page_size = portrait(A4)

    file_name = f"{orientation}.pdf"

    pdf = canvas.Canvas(
        file_name,
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
        "width": width,
        "height": height
    }


@router.get("/generate-watermarked-pdf")
def generate_watermarked_pdf(orientation: str = "portrait"):

    source_pdf = f"{orientation}.pdf"

    if not os.path.exists(source_pdf):
        raise HTTPException(
            status_code=404,
            detail="Generate PDF first"
        )

    reader = PdfReader(source_pdf)
    first_page = reader.pages[0]

    # Get page size dynamically
    page_width = float(first_page.mediabox.width)
    page_height = float(first_page.mediabox.height)

    # Create watermark
    packet = BytesIO()

    watermark_canvas = canvas.Canvas(
        packet,
        pagesize=(page_width, page_height)
    )

    watermark_canvas.setFillColor(
        Color(0.7, 0.7, 0.7, alpha=0.3)
    )

    watermark_canvas.setFont(
        "Helvetica-Bold",
        40
    )

    # Center of page
    center_x = page_width / 2
    center_y = page_height / 2

    watermark_canvas.saveState()

    watermark_canvas.translate(
        center_x,
        center_y
    )

    watermark_canvas.rotate(45)

    watermark_canvas.drawCentredString(
        0,
        0,
        "CONFIDENTIAL"
    )

    watermark_canvas.restoreState()

    watermark_canvas.save()

    packet.seek(0)

    watermark_pdf = PdfReader(packet)

    writer = PdfWriter()

    for page in reader.pages:
        page.merge_page(
            watermark_pdf.pages[0]
        )
        writer.add_page(page)

    output_file = f"watermarked_{orientation}.pdf"

    with open(output_file, "wb") as f:
        writer.write(f)

    return {
        "fetch_flag": "1",
        "message": "Watermark Added Successfully",
        "file_name": output_file,
        "page_width": page_width,
        "page_height": page_height
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

    # Create output directory
    output_dir = "app/assets/generated_pdfs"
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename
    file_name = f"LIMS_{int(time.time())}.pdf"
    file_path = os.path.join(output_dir, file_name)
    

    # # Save PDF
    # with open(file_path, "wb") as pdf_file:
    #     pisa.CreatePDF(
    #         html,
    #         dest=pdf_file
    #     )
    # # Check for success
    # if not os.path.exists(file_path):
    #     raise HTTPException(
    #         status_code=500,
    #         detail="PDF generation failed"
    #     )
    
    with open(file_path, "wb") as pdf_file:
        result = pisa.CreatePDF(html, dest=pdf_file)

    if result.err:
        raise HTTPException( status_code=500, detail="PDF generation failed")

    return {
        "fetch_flag": "1",
        "message": "PDF generated successfully",
        "file_name": file_name,
        "pdf_url": f"app/assets/generated_pdfs/{file_name}",
    }

def render_label(template_name: str, item1: str = "", item2: str = "", item3: str = ""):
    template = templates.get_template(template_name)
    return template.render(
        sub_item_1=item1,
        sub_item_2=item2,
        sub_item_3=item3
    )