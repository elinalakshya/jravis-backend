import os
import uuid
import zipfile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "factory_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_product():
    title = "Morning Routine Planner – Printable Productivity Toolkit"

    description = (
        "Morning Routine Planner designed to help users stay consistent,\n"
        "organized, and achieve measurable improvement.\n\n"
        "Use this planner daily:\n"
        "- Morning goals\n"
        "- Focus block\n"
        "- Reflection notes\n\n"
        "Stay consistent. Stay focused."
    )

    price = 149

    uid = uuid.uuid4().hex[:8]
    pdf_name = f"planner_{uid}.pdf"
    zip_name = f"planner_pack_{uid}.zip"

    pdf_path = os.path.join(OUTPUT_DIR, pdf_name)
    zip_path = os.path.join(OUTPUT_DIR, zip_name)

    # ---------- CREATE PDF ----------
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    y = height - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, title)

    y -= 40
    c.setFont("Helvetica", 11)
    for line in description.split("\n"):
        c.drawString(50, y, line)
        y -= 16

    c.showPage()
    c.save()

    # ---------- CREATE ZIP ----------
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(pdf_path, arcname=pdf_name)

  return {
    "title": title,
    "price": price,
    "zip_path": zip_filename
}

